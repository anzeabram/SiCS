# SiCS - Slovenian Cave Survey

This is a repository for underwater survey projects run in Slovenia. Each folder represents a cave project run on voluntary basis by avid cave divers. Each folder contains:
-	raw survey data (.xls exports from MNemo device for UW survey and plaintext from DistoX laser measurements for dry sections.)
-	formatted survey files and project files for “Walls”, a dedicated program for cave survey data management (free: https://texasspeleologicalsurvey.org/software/walls/tsswalls.php)
-	vector graphic files and .pdf exports of finalized maps (Adobe Illustrator)

With this repository, we aim to preserve the raw data and allow for further collaboration and advancement in exploration and survey efforts. If you would like to contribute, let us know (find us on social networks)

Moreover, we recently (late 2025) began to experiment with Therion workflow. This would allow us to keep all the data (survey data and the drawings) in plain formats, without the need of propertary software and easily integrate to GIS. Our Therion 'playground' can be found in [playground](./playground) folder, and the process documented below.

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

- [Therion](https://therion.speleo.sk/download.php) - The main compiler. It includes xtherion (a GUI) and Loch for displaying 3d exports. Installation on Windows and Linux is trivial. Users using macOS can either use [Homebrew](https://github.com/ladislavb/homebrew-therion) or compile it themselves. You can also find a [Therion docker container](https://github.com/matteopic/therion-container).

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

## Adding data

You have produced some survey data, either by DistoX (dry sections) or with MNemo (submerged passages). TopoDroid can export in Therion format, but you will have to covert the data from MNemo. First create a new folder for a given passage, following `data/{cave}/{year}/{passage}` hierarchy. Next, use a `.th` template from `templates` folder and fill in the metadata along with the survey data. Name the passage with lower case name (as far as possible, use dashes (-) as spaces). The typical `.th` survey file looks like this:

```
encoding  utf-8

survey sump01 -title "Sump 1"

# th2 includes with scraps

input sump01-p.th2
input sump01-e.th2

# map definitions, needs to include all relevant scraps

map m-sump01-p -projection plan
     sump01-1p
endmap

map m-sump01-e -projection extended
    sump01-1e
endmap

centerline
    # team members and roles [instruments, notes, assistant, pictures, dimensions]
    team "Name Surname" instruments
    team "Name Surname" notes

    # date of survey
    date 2022.8.26

    # depths as positive numbers
    calibrate depth 0 -1
    units length depth meters
    units compass degrees
    data diving from to length compass fromdepth todepth left right up down 
    # direction for extended elevation view
    extend right
    
    0 1 6 152 0 1 0.5 10 15 4
    1 2 3 120 1 3 0 10 15 4
    2 3 3 120 3 4 0 2.8 5 2.1
    3 4 3.3 88 4 6 2.2 2.3 5.4 0.6
    4 5 3 74 6 7 3.8 2.1 2.7 0
    5 6 3 118 7 7.5 1.6 1.9 3.3 0
    6 7 6 118 7.5 5 0.8 0.9 3.4 0
    7 8 6 165 5 4 0 2 3.3 0.5
    8 9 2 112 4 3 2.1 2 0 0
    9 10 3 90 3 1 2 4 0 1
    10 11 3 110 1 0.5 0 5 0 0
    11 12 6 140 0.5 0 4 7 4 4

    station 1 "Comment 1"
endcenterline

endsurvey
```

`calibrate depth 0 -1` allows for dpeths as positive integers (used for UW survey)

Find the `{cave}.th` file in the `data/{cave}` folder. This file contains a series of input `./year/passage/passage.th` commands to tell the therion compiler to include the relevant survey data. Adding the command input `./year/passage/my_new_passage.th` to this file in the correct year folder is necessary, but we now need to connect the new data to an existing point in the survey, i.e. equate.

Below the input blocks, you will find a series of `equate` commands, this is where you can tie in your new cave passage to the existing centrelines.

The main `{cave}.th` file will therefore look similar to this (a template from `tempaltes` folder):

```
encoding  utf-8

survey cave01 -title "Cave 1"

	# input the map definitions
	input ./cave01-p.thm #plan view
	input ./cave01-e.thm #extended elevation view

    # input the individual survey data files
    input ./2025/sump01/sump01.th
    input ./2025/sump02/sump02.th
    input ./2025/dry01/dry01.th

    # equate stations between different surveys
    equate 12@sump01 0@sump02
    equate 12@sump02 1@dry01

    # connect the individual scraps - plan view
    join sump01-1p@sump01 sump02-1p@sump02
    join sump02-1p@sump02 dry01-1p@dry01

    # connect the individual scraps - extended view
    join sump01-1e@sump01 sump02-1e@sump02
    join sump02-1e@sump02 dry01-1e@dry01

    centerline
        cs epsg:3912
        station 0@sump01 "Cave 1 entrance" entrance
        fix 0@sump01 445791 89768 293
    endcenterline
    
endsurvey
```

### Adding scraps

The steps go as follow:

- generate `.th2` files for plan and extended view from a newly included survey (passage) via python script. Note that there shouldn't be any `.th2` includes within the `passage01.th` file. Comment them out. Example:

```
python3 scripts/create_2d.py data/cave01/cave01.th passage01@cave01 --projection plan
```

- draw walls and other features to both `.th2` files in Inkscape
- include both `.th2` files to a `.th` survey file of a passage (check `templates`)
- include scraps in plan and extended view maps in `{cave}.thm` file
- join the scraps within `{cave}.th` file

## Drawing in Inkscape

Open the `{passage}-p.th2` file in Inkscape. You should see a centreline of the passage you're editing with some station objects at each node.

Have a look at the layers panel, there should be four:

- **{passage}-1p** : This contains the stations and is where you should draw things like walls.
- **DELETE-ME-survey-legs** : Shows the survery legs to help you draw. This should be deleted or not saved after the passage is drawn.
- **Symbol legend** : Displays all the possible Therion objects you can place. The intention is that you can copy and paste them from here into the {passage}-1p layer. You should always hide this layer when you are done.
- **Background images** : Somewhere to import images to help drawing (old surveys, uw drawings).

Create hotkeys for 'Set Point/Line/Area type' within Inkscape as you will be using those a lot.

### Drawing walls
Use the pen tool to draw the walls around the stations. Make sure the nodes are all connected in one long polygon, except where passages will join in from other sides. In order to set the type of lines as walls or pits or anything else you fancy, select for instance all the lines that you wish to 'set', navigate to Extensions>Therion>Set Line Type>... choose from the dropdown menu and click 'Apply' and let it run. This usually changes the styling of the line, depending on what you've chosen. Wall lines do not change too much, but pits are now barbed, chimneys are steepled lines, rock-borders are slightly thinner etc... Make sure that the 'tails' at the ends of wall feature point inwards.

### Drawing points
You can choose them from the `Symbol Legends` layer, and copy paste them wherever they are needed (but it needs to be in the scrap layer). I tend to use: 'narrow-end' (=) or 'continuation' (?) often. You can reset the type to anything you want using Extensions>Therion>Set Point Type and change the storming lead to a boulder choke and so forth.

### Add labels
I usually just draw a rectangle (does not matter the size or the styling), select the rectangle, navigate to object properties and write the label there.

Syntax: `point label -scale <xs/s/m/l/xl> -align <br/r/t/b/tl/tr/bl> -text [mylabel]` Choose the scale of the point label carefully.

### Add depth/altitude

The depth of the passage can be displayed via point altitude feature. The data is drawn from the survey data.

### Drawing cross-sections

Drawing cross-sections consists of two parts. Firstly, you need to create a new layer (scrap) named `scrap passage01-1cs -projection none -scale [7.87402 1 m]` in which to draw the outline of the passage. Secondly, position drawn outline inside your original plan view scrap using `point section -scrap name-of-the-scrap`. Draw `line section` as brezier line. It takes "begin" (beginning of the section line), "end", "both", "none" and "point" as arguments for arrows. Section lines are drawn differently than regular lines. When you place the line, make it a bezier curve and place the control handle that you use to bend the line around next to the spot where you want it to disappear. Do that on both ends of the line. The portions of the section line between the "inside" end points of any two consecutive control points are not drawn. You can also draw poligonal section lines.

### Drawing permanent/temporary line

First copy the survey legs from `DELETE-ME-survey-legs` layer into your scrap layer. Change them from `line survey` to `line u:diveline` or `line u:jumpline` if you want to desplay a dashed line (for jumps or entrance area where reel is primarely used).

### Labeling restrictions

Use user-defined point symbols with arguments `u:r` or `u:rsm` for sidemount restriction. Example:

```
point 20.3029 107.278 u:r
```

### Gradient symbols

Add gradients (slope) as `point gradient` and rotate acordingly.

## Additional helpers

### Sketches for UW drawings

Use `sketch.thconfig` to produce a `.svg` file export with a stick map of the survey data on a 1x1 m grid. Open it in Inkscape and rotate accordingly.

### Coloring

On the links below you can find a color brewers to be used with carographical data

- [Colorbrewer](https://colorbrewer2.org)
- [Colorcodes](https://colorcodes.io)

### Custom tags

Custom attributes  Objects survey, centreline, scrap, point, line, area, map and surface can contain userdefined attributes in a form -attr <name> <value>. <name> may contain alphanumeric  characters, <value> is a string.  The custom attributes are used in map exports depending on the output format:  • in shapefile export they are written directly to the associated dbf file,  • in maps generated using METAPOST (PDF, SVG) the attributes are written in the  METAPOST source file as strings (named like ATTR_<name>) and can be evaluated and  used by the user to define symbols in macros.

### Use 'debug on' to check scrap stitching

- red lines: the original scraps (after rotation and rescaling);
- blue lines: the scraps adjusted to the "station" positions (before the joins);
- red points: original positions of the "station" points;
- yellow points connected by yellow lines: initial positions of the pairs of points with maximal distorsion;
- black points connected by black lines: final position of pairs of points with maximal distorsion;
- orange points: points with maximal change of their distance, in the transformation;
- yellow lines between yello and black points: displacement of these points.

### Add pdfs and images to the map

You can insert a picture in the map header with the following map-image command. Images in pdf, png, jpg are supported. Therefore you can insert photos, logos, and also a map, say the extented elevation on the page of the plan. For example,
```
  -layout-map-image 0 50 ne "./elev.pdf"
```

### Layers

Every graphical element belongs to a layer (or group). The graphical elements are rendered in the cave map following the order of the layers. There are five layers:
* bottom, the lowest layer. It contains only elements that have the option -place bottom.
* default-bottom. It contains the areas.
* default;
* default-top. This contains the ceiling-step and chimney elements by default.
* top. It contains the elements that have the option -place top.

### Groups

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

### Point subtypes

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

### Column in the passage

The hole inside the area is bordered by a "wall" line (with "-outline in").

### Labels

Labels are points of type label. The text to display must be written in the "options" textbox as -text .... Enclose the text in double quotes if it contains blank spaces. You may use HTML tags to format the text: <it>for italics, <bf>for boldface, and so on. Use <br>for a new-line, and <right>to right justify the text. The switch <lang:XX>specifes the language. The position of the text can be aligned to the placed point with the "-align" option. This takes values "r" (right), "l" (left), "t" (top), "b" (bottom), "c" (center), "tl", "tr", etc. For example "-align tl" means that the text is placed to the top and left of the point, ie, the point is the bottom-right corner of the text rectangle.


