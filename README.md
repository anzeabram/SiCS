# SiCS - Slovenian Cave Survey

This is a repository for underwater survey projects run in Slovenia. Each folder represents a cave project run on voluntary basis by avid cave divers. Each folder contains:
-	raw survey data (.xls exports from MNemo device for UW survey and plaintext from DistoX laser measurements for dry sections.)
-	formatted survey files and project files for “Walls”, a dedicated program for cave survey data management (free: https://texasspeleologicalsurvey.org/software/walls/tsswalls.php)
-	vector graphic files and .pdf exports of finalized maps (Adobe Illustrator)

With this repository, we aim to preserve the raw data and allow for further collaboration and advancement in exploration and survey efforts. If you would like to contribute, let us know (find us on social networks)

Moreover, we recently (late 2025) began to experiment with Therion workflow. This would allow us to keep all the data (survey data and the drawings) in plain formats, without the need of propertary software. Our Therion 'playground' can be found in [playground](./playground) folder, and the process documented below.

Contributors:
- Anže Abram
- Sebastjan Gantar
- Alan Bizjak

# How to work with Therion

During the learning process, several sites and repositories have been of tramendous help. Several pieces of text below are taken from those sites.

- [Migovec Resurvey Project](https://github.com/tr1813/migresurvey) The repository structure, text below and layouts were *heavily* inspired by their work.
- [Speleo Philippines Expeditions](https://github.com/speleo/SpeleoPhilippines/tree/master)
- [Therion Wiki](https://therion.speleo.sk/wiki/start)
- [Therion by examples](http://marcocorvi.altervista.org/caving/tbe/fulltoc.htm)
- [The Therion book](http://therion.speleo.sk/downloads/thbook.pdf)

## Prerequisites

The data is stored in plain text and needs to be compiled with dedicated software. Therion GUI interface is rather archaic and can be avoided completly by the use of extensions.

For compiling and exporting:

- [Therion](https://therion.speleo.sk/download.php) - The main compiler. It includes xtherion (a GUI) and Loch for displaying 3d exports. Installation on Windows and Linux is trivial. Users using macOS can either use [Homebrew](https://github.com/ladislavb/homebrew-therion) or compile it themselves.

To compile therion on macOS via cmake, first clone the repository and run the following commands.

```
cd therion
mkdir build
cd .
cmake -S . -B build
cd build
make
sudo make install
```

For drawing we are using Inkscape and the Therion Inkscape extensions because we think its nicer than using the Therion editor:

- [Inkscape](https://inkscape.orghttps//github.com/iccaving/migovec-survey-data/release/) - Vector drawing program
- [Inkscape Therion Extensions](https://github.com/speleo3/inkscape-speleo/) - The extensions that allow you to draw Therion scraps in Inkscape.

For editing the text files:

- [VSCode](https://code.visualstudio.com/Download)
- [VSCode Therion Extension](https://marketplace.visualstudio.com/items?itemName=rhystyers.therion) You can also find this one within VSCode Marketplace.
- [VSCode Python Extension](https://marketplace.visualstudio.com/items?itemName=ms-python.python) We use python scripts to create .th2 files from survey data (original scripts from [Migovec Survey](https://github.com/tr1813/migresurvey/tree/master/scripts)).

## Therion Glossary

Therion has a complex vocabulary of its own so here is a basic translation.

### Internal Data

- **survey** : main data structure, which can be nested ad nauseam to represent karst areas, caves or passages. Each survey has an object id, which must be unique within the scope of the higher level survey. Likewise, any object within a survey has unique id (from stations, to maps, scraps). This allows for simple naming of stations within survey files.
- **centreline** : survey data specification., with syntex mostly derived from Survex. DistoX export will add splays to this section as well.
- **scrap** : The most basic drawing element, a piece of 2D map (plan, extended, or none - used for drawing cross-sections). It will consist of the walls and stations of the passage as well as lots of extra information like boulders, pits, passage gradients etc. A single set of survey data (a single passage) can have many scraps associated with it. It is often good to split the drawing over many scraps as this allows Therion to do clever things (like depth colouring). Scraps cannot overlap themselves.
- **map** : The higher level drawing element. A map can be made of scraps, or it can be a map of maps. It can also incorporate stick map of undrawn passages with correct layout options. Maps are how you collect individual drawn passages into larger blocks. For example a cave like ```Cave01``` will have its scraps (that is, drawings from individual passages like `m-passage01-p`, `m-passage02-p`,...) collected in a map called `m-all-p` (`-p` for plan view, `-e` for extended). The maps can be nested and allow for smart exclusion or inclusion of specific sections of the cave.

### Exported Data

Therion can export to a number of formats.

- **Map** : A 2D representation of the survey data. Usually a `.pdf` or `.svg`.
- **Atlas** : A 2D representation of the survey data split into pages for convenient printing.
- **Model** : A 3D representation of the survey data. Usually a `.3d` or `.lox` file viewed in aven or loch.
- **Database** : Survey data dumped to a database for whatever reason. Usually a `.sql` file.
- **Esri** : Shapefile export that can be inported to GIS software (e.g. [QGIS](https://github.com/qgis/QGIS))

### Other Key Words

- **equate** : An equate lets Therion know that two stations are the same (that they are joined). This is how basically all the export formats are constructed.
- **join** : A join lets Therion know that two scraps, or lines should be joined. It does its best to match up any walls that are nearby each other to create a seamless passage when exporting maps and atlases. You can also specify at how many point the scraps should be joined.

## Repository and File Structure

It can be hard to know where to start in a repository so here is an overview of how things are organised and what various files and folders are for.

### Survey data

The raw data, usually created in the cave, or shortly after. These are within the `data\{cave}\{year}\{passage}` directories.

These will likely represent single pushing trips.

- `.th` files contain the survey data (between centreline/endcentreline flags)
- `.th2` files contain the scraps (drawings beginning with scrap `{scrap-id}/endscrap` flags)
The `.th` will probably also enclose any scraps (in the `.th2`) within the passage as a named map. This can be autogenerated by Topodroid, VSCode Inkscape plugin or added manually.

### Higher level data

In the `data\{cave}` folders you will find `.th` files that define how these individual passages are connected.

- `{name}.th` will be used to defined equates in the survey and join scraps between passages.
- `{name}.thm` will be used to combine individual passage maps into larger maps. If maps are not defined, all survey within the scope of the cave are used. The use of the maps allows for easy adjustments and incorporation of stick maps for undrawn passages.

In the `{name}.th` file, passages are arranged by year of discovery. In the `{name}.thm` file, passage map definitions are ordered by cave sub-region, and these subregions are themselves ordered into a map definition for the cave (a high level `m-all-p`, within the scope of the cave).

### Exports

With the data thus organised you can export maps in pdf and svg files and models in .3d and lox files. This is done through a further two types of file.

In the `configs` folder there are `.thconfig` files. These are more similar to a shell script if you are familiar with those. They contain commands to produce output files like pdfs etc. They combine the named maps and layouts to make the output.

In the `layouts` folders there are layout files (`.thl`) these are complicated but they basically just define which symbols should be on the map and how they should be like. i.e. should you show mineral symbols, how thick should pit lines be, what colour are waterfalls. They can ve included and reused between different cave exports.

## How to export data

### Using existing configs

The easy way is to find yourself the config file that already does what you want. You can find config templates in `configs` folder and `.theconfig` files for specific cave in their top folder. You can either run it from VSCode through the plugin or in command line. It outputs to `outputs` folder.

```
therion data/cave01/cave01.thconfig
```

### Make your own config

You can easily create exports of your own. Every `.thconfig` file follows a similar patter:

- specify the data source (the `.th` file)
- include layout potions from `.thl` files and include them to the layout that will be used in the export
- select which map from the cave you wish to export
- define export options and the path where they should be saved

A template config file will look like this:

```
encoding  utf-8

source cave01.th

input ../../layouts/translations-si.thl
input ../../layouts/base-p.thl

layout plan
  copy base-p

  doc-author "Name Surname"
  doc-title "Map of Cave 01"

  # Grid zero for altitude display
  cs epsg:3912
  grid-origin 0 0 293 m

  # symbol-hide line survey
  # symbol-hide point station
endlayout

select m-all-p@cave01

export map -projection plan -output ../../outputs/cave01-p.pdf -layout plan
```

## Coloring

On the links below you can find a color brewers to be used with carographical data

[Colorbrewer](https://colorbrewer2.org)
[Colorcodes](https://colorcodes.io)

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

## Add pdfs and images to the map

You can insert a picture in the map header with the following map-image command. Images in pdf, png, jpg are supported. Therefore you can insert photos, logos, and also a map, say the extented elevation on the page of the plan. For example,
  -layout-map-image 0 50 ne "./elev.pdf"

## Layers

Every graphical element belongs to a layer (or group). The graphical elements are rendered in the cave map following the order of the layers. There are five layers:
* bottom, the lowest layer. It contains only elements that have the option -place bottom.
* default-bottom. It contains the areas.
* default;
* default-top. This contains the ceiling-step and chimney elements by default.
* top. It contains the elements that have the option -place top.

## Groups

The "group" type defines groups of symbols. The possible groups are
* "group centerline"
    * subgroups: "surface-centerline", "cave-centerline"
    * lines: survey:surface survey:cave
    * points: surface-station cave-station
* "group sections":
    * lines: section
    * points: section
* "group water"
    * lines: water-flow
    * points: water-flow, water, sink, spring
    * areas: water, sump
* "group sediments"
    * lines: wall:sand, wall:clay
    * points: sand, clay, clay-tree, raft, raft-cone, guano
    * areas: sand, clay,
* "group passage-fills"
    * lines: rock-border, rock-edge, water-flow
    * points: bedrock, sand raft, clay, pebbles, debris, blocks, water, ice, guano, snow
    * areas: water, sump, bedrock, blocks, clay, debris, ice, pebbles, sand, snow
* "group equipment"
    * lines: rope
    * points: anchor, rope, fixed-ladder, rope-ladder, steps, bridge, traverse, camp, no-equipement
* "group speleothems"
    * lines: flowstone, moonmilk
    * points: flowstone, moonmilk, stalactite, stalagmite, pillar, curtain, helictite, soda-straw, crystal, wall-calcite, popcorn, disk, gypsum, gypsum-flower, aragonite, cave-pearl, rimstone-pool, rimstone-dam,
    * areas: flowstone, moonmilk
* "group ice"
    * lines: wall:ice
    * points: ice, ice-stalactite, ice-stalagmite, ice-pillar, snow,
    * areas: ice, snow


## Point subtypes

Certain points and lines can be further qualified,
* "point flags:flag_name"
    * flag_name: entrance, continuation, sink, spring, doline, dig, air-draught, arch, overhang
* "line wall", "line wall:subtype"
    * subtype: bedrock, blocks, clay, debris, ice, pebbles, presumed, sand, underlying, unsurveyed, pit, overlying, moonmilk, flowstone
* "line water-flow", "line water-flow:subtype"
    * subtype: conjectural, intermittent, permanent
* "line border", "line border:subtype"
    * subtypes: temporary, visible
* "line survey", "line survey:subtype"
    * subtype: surface, cave
* "point station", "point station:subtype"
    * subtype: fixed, natural, painted, temporary, surface station, cave station
* "point air-draught", "point air-draught:subtype"
    * subtypes: winter, summer
* "point water-flow", "point water-flow:subtype"
    * subtypes: intermittent, paleo, permanent
* "point passage-height", "point passage-height:specification"
    * specification: positive, negative, both, unsigned
* "point height", "point height:specification"
    * specification: positive, negative, unsigned

## Column in the passage

the hole inside the area is bordered by a "wall" line (with "-outline in").

## Labels

Labels are points of type label. The text to display must be written in the "options" textbox as -text .... Enclose the text in double quotes if it contains blank spaces. You may use HTML tags to format the text: <it>for italics, <bf>for boldface, and so on. Use <br>for a new-line, and <right>to right justify the text. The switch <lang:XX>specifes the language. The position of the text can be aligned to the placed point with the "-align" option. This takes values "r" (right), "l" (left), "t" (top), "b" (bottom), "c" (center), "tl", "tr", etc. For example "-align tl" means that the text is placed to the top and left of the point, ie, the point is the bottom-right corner of the text rectangle.


