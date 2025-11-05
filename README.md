# SiCS - Slovenian Cave Survey

This is a repository for underwater survey projects run within Slovenia. Each folder represents a cave project run on voluntary basis by avid cave divers. Each foder contains:
-	raw survey data (.xls exports from MNemo device for UW survey and plaintext from DistoX laser measurements for dry sections.)
-	formatted survey files and project files for “Walls”, a dedicated program for cave survey data management (free: https://texasspeleologicalsurvey.org/software/walls/tsswalls.php)
-	vector graphic files and .pdf exports of finalized maps (Adobe Illustrator)

With this repository, we aim to preserve the raw data and allow for further collaboration and advancement in exploration and survey efforts. If you would like to contribute or work on the data, drops us a dm.

Contributors:
- Anže Abram
- Sebastjan Gantar
- Alan Bizjak

# Placeholder

## Coloring

On the links below you can find a color brewers to be used with carographical data

[Colorbrewer](https://colorbrewer2.org)
[Colorcodes](https://colorcodes.io)

## Resources for metapost code and layouts

- https://therion.speleo.sk/wiki/metapost
- https://github.com/speleo/SpeleoPhilippines/tree/master/CodeLibrary
- https://therion.speleo.sk/wiki/templates
- https://therion.speleo.sk/wiki/drawingchecklist


## macOS install

```
cd therion
mkdir build
cd .
cmake -S . -B build
cd build
make
sudo make install
```

## Custom tags

Custom attributes  Objects survey, centreline, scrap, point, line, area, map and surface can contain userdefined attributes in a form -attr <name> <value>. <name> may contain alphanumeric  characters, <value> is a string.  The custom attributes are used in map exports depending on the output format:  • in shapefile export they are written directly to the associated dbf file,  • in maps generated using METAPOST (PDF, SVG) the attributes are written in the  METAPOST source file as strings (named like ATTR_<name>) and can be evaluated and  used by the user to define symbols in macros.

## Use 'debug on' to check scrap stitching

* red lines: the original scraps (after rotation and rescaling);
* blue lines: the scraps adjusted to the "station" positions (before the joins);
* red points: original positions of the "station" points;
* yellow points connected by yellow lines: initial positions of the pairs of points with maximal distorsion;
* black points connected by black lines: final position of pairs of points with maximal distorsion;
* orange points: points with maximal change of their distance, in the transformation;
* yellow lines between yello and black points: displacement of these points.