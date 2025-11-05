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

