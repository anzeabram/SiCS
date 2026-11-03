#!/usr/bin/env python3
"""Convert a diving survey XLSX export into a Therion .th centerline.

Only Python's standard library is required. Expected Excel columns:
TypeShot, Length, Depth IN, Depth OUT, Heading IN, Heading OUT.

Example:
    python xlsx_to_therion.py meritve2026.10.17.xlsx
    python xlsx_to_therion.py survey1.xlsx survey2.xlsx --sheet B04

Each output is placed beside its input and uses the same basename with .th.
"""

from __future__ import annotations

import argparse
import math
import posixpath
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from zipfile import ZipFile

MAIN_NS = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
DOC_REL_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"
M = "{" + MAIN_NS + "}"


def column_number(cell_reference: str) -> int:
    """Convert an Excel address such as 'AB123' to a zero-based column."""
    letters = re.match(r"[A-Z]+", cell_reference.upper())
    if letters is None:
        raise ValueError(f"Invalid Excel cell reference: {cell_reference!r}")
    result = 0
    for letter in letters.group():
        result = result * 26 + ord(letter) - ord("A") + 1
    return result - 1


def read_excel_rows(path: Path, sheet_name: str | None):
    """Read XLSX cell values as numbered, sparse rows, without dependencies."""
    with ZipFile(path) as archive:
        names = set(archive.namelist())
        shared_strings = []
        if "xl/sharedStrings.xml" in names:
            shared = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            shared_strings = [
                "".join(t.text or "" for t in si.iter(M + "t"))
                for si in shared.findall(M + "si")
            ]

        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        relationships = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relation_targets = {
            entry.attrib["Id"]: entry.attrib["Target"]
            for entry in relationships.findall("{" + PKG_REL_NS + "}Relationship")
        }
        sheets = workbook.find(M + "sheets")
        choices = [] if sheets is None else sheets.findall(M + "sheet")
        if not choices:
            raise ValueError("The XLSX workbook contains no worksheets")

        selected = next((s for s in choices if s.attrib["name"] == sheet_name), None) if sheet_name else choices[0]
        if selected is None:
            raise ValueError(f"Worksheet {sheet_name!r} not found; available: "
                             + ", ".join(s.attrib["name"] for s in choices))
        chosen_name = selected.attrib["name"]
        rel_id = selected.attrib["{" + DOC_REL_NS + "}id"]
        target = relation_targets[rel_id]
        member = target.lstrip("/") if target.startswith("/") else posixpath.normpath(posixpath.join("xl", target))

        worksheet = ET.fromstring(archive.read(member))
        data = worksheet.find(M + "sheetData")
        rows = {}
        if data is None:
            return chosen_name, rows
        for row in data.findall(M + "row"):
            row_num = int(row.attrib["r"])
            cells = {}
            for cell in row.findall(M + "c"):
                col = column_number(cell.attrib["r"])
                data_type = cell.attrib.get("t", "n")
                raw = cell.findtext(M + "v")
                if data_type == "inlineStr":
                    value = "".join(t.text or "" for t in cell.iter(M + "t"))
                elif raw is None:
                    continue
                elif data_type == "s":
                    value = shared_strings[int(raw)]
                elif data_type in {"str", "e"}:
                    value = raw
                elif data_type == "b":
                    value = raw == "1"
                else:
                    value = float(raw)
                cells[col] = value
            rows[row_num] = cells
        return chosen_name, rows


def normalize_heading(name: object) -> str:
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def as_number(value: object, row_num: int, field: str) -> float:
    try:
        number = float(str(value).replace(",", "."))
    except (ValueError, TypeError):
        raise ValueError(f"Row {row_num}: missing/invalid {field}: {value!r}") from None
    if not math.isfinite(number):
        raise ValueError(f"Row {row_num}: nonfinite {field}: {value!r}")
    return number


def circular_average(a: float, b: float) -> tuple[float, float]:
    """Return mean azimuth and smaller separation in degrees.

    Both input headings point in the same direction, as in this XLSX export.
    E.g. 359 and 1 degrees average to 0 (not 180).
    """
    if not 0 <= a <= 360 or not 0 <= b <= 360:
        raise ValueError(f"Headings must be in [0, 360] degrees: {a}, {b}")
    signed_difference = (b - a + 180) % 360 - 180
    difference = abs(signed_difference)
    if math.isclose(difference, 180.0, abs_tol=1e-8):
        raise ValueError(f"Cannot average exactly opposite headings: {a}, {b}")
    return (a + signed_difference / 2) % 360, difference


def survey_identifier(filename: str) -> str:
    """Make a Therion-friendly survey identifier from the file stem."""
    result = re.sub(r"[^A-Za-z0-9_-]+", "-", filename).strip("-")
    if not result:
        raise ValueError("Cannot derive a survey identifier from the filename")
    return "s-" + result if result[0].isdigit() else result


def convert(source: Path, sheet: str | None = None, warn_degrees: float = 20.0) -> tuple[Path, int, list]:
    sheet_title, rows = read_excel_rows(source, sheet)
    required = ("typeshot", "length", "depthin", "depthout", "headingin", "headingout")
    header_row = None
    columns = None
    for row_num, cells in sorted(rows.items()):
        col_names = {normalize_heading(v): i for i, v in cells.items()}
        if all(field in col_names for field in required):
            header_row, columns = row_num, col_names
            break
    if header_row is None or columns is None:
        raise ValueError(f"{source}: missing expected survey header columns: {', '.join(required)}")

    date_match = None
    for row_num, cells in sorted(rows.items()):
        if row_num >= header_row:
            break
        for cell in cells.values():
            match = re.search(r"\bDate\s*:\s*(\d{4})[-./](\d{1,2})[-./](\d{1,2})\b", str(cell), re.IGNORECASE)
            if match:
                date_match = match
                break
        if date_match:
            break
    if date_match is None:
        raise ValueError(f"{source}: cannot find 'Date: YYYY-MM-DD' above the header")
    survey_date = ".".join(str(int(part)) for part in date_match.groups())

    result = []
    warnings = []
    for row_num, cells in sorted(rows.items()):
        if row_num <= header_row:
            continue
        kind = str(cells.get(columns["typeshot"], "")).strip().lower()
        if not kind:
            continue
        if kind == "eoc":  # End-of-cave marker is not an actual survey leg.
            break
        if kind != "std":
            raise ValueError(f"Row {row_num}: unsupported TypeShot {kind!r}; refusing to silently omit it")

        length = as_number(cells.get(columns["length"]), row_num, "Length")
        depth_in = as_number(cells.get(columns["depthin"]), row_num, "Depth IN")
        depth_out = as_number(cells.get(columns["depthout"]), row_num, "Depth OUT")
        az_in = as_number(cells.get(columns["headingin"]), row_num, "Heading IN")
        az_out = as_number(cells.get(columns["headingout"]), row_num, "Heading OUT")
        if length <= 0:
            raise ValueError(f"Row {row_num}: leg length must be positive")
        try:
            compass, spread = circular_average(az_in, az_out)
        except ValueError as exc:
            raise ValueError(f"Row {row_num}: {exc}") from exc
        if spread > warn_degrees:
            warnings.append((row_num, az_in, az_out, spread))

        from_station = len(result)
        result.append(
            f"    {from_station}  {from_station + 1}  {length:.2f}  "
            f"{compass:.2f}  {depth_in:.2f}  {depth_out:.2f}"
        )
    if not result:
        raise ValueError(f"{source}: no standard survey legs were found")

    # No station labels, teams or scrap references are invented when absent.
    survey_id = survey_identifier(source.stem)
    survey_title = sheet_title.replace('"', "'")
    lines = [
        "encoding  utf-8",
        "",
        f'survey {survey_id} -title "{survey_title}"',
        "",
        "centerline",
        f"    date {survey_date}",
        "    # Positive source depths are kept in the same convention as the example.",
        "    calibrate depth 0 -1",
        "    units length depth meters",
        "    units compass degrees",
        "    data diving from to length compass fromdepth todepth",
        "    extend right",
        "",
        "    # Compass = circular mean of Heading IN and Heading OUT (degrees).",
        *result,
        "",
        "endcenterline",
        "",
        "endsurvey",
        "",
    ]
    output = source.with_suffix(".th")
    output.write_text("\n".join(lines), encoding="utf-8")
    return output, len(result), warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path, help="Input .xlsx files")
    parser.add_argument("--sheet", help="Worksheet name (default: first sheet)")
    parser.add_argument("--warn-degrees", type=float, default=20.0,
                        help="Warn if headings differ by more than N degrees (default: 20)")
    args = parser.parse_args()
    for path in args.files:
        if path.suffix.lower() != ".xlsx":
            parser.error(f"Expected .xlsx file, got {path}")
        try:
            output, count, warnings = convert(path, args.sheet, args.warn_degrees)
        except (OSError, KeyError, ValueError, ET.ParseError) as exc:
            print(f"ERROR: {path}: {exc}", file=sys.stderr)
            return 1
        print(f"Created {output} ({count} survey legs)")
        if warnings:
            print(f"WARNING: {len(warnings)} legs have IN/OUT azimuth differences greater "
                  f"than {args.warn_degrees:g}°:", file=sys.stderr)
            for row_num, first, second, spread in warnings:
                print(f"  Excel row {row_num}: {first:g}° vs {second:g}° (difference {spread:.1f}°)",
                      file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
