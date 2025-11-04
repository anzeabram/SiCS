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

# Move to Therion

We are in the process of moving from Walls/Illustrator workflow to Therion. The testing data is in 'playground' folder. There are several aspects that still need to be solved before the move:

- how to scale cross-sections in Inkscape
- how to automatically generate a border around cross-section views (scraps with -projection none arguments)
- finalize the layouts for plan and extended view (match the symbols with those from the Illustrator)
- figure out how to combine scraps with th2 data and those with only the centerline (add an intermediate 'maps' workflow that combines all the drawn scraps and centerline)
- figure out a QGIS (server) workflow, WMS, read-only public options and read/write for survey team (Erika Kozamernik, gozdis?). We probably don't need to export all the features, only the centerline and walls. Check https://github.com/Alex38Lyon/QGis_Therion/blob/main/README.en.md
- (optional) modify 'point altitude' so it displays negative values as positives with a line above, in red
- modify labels to take the 'color' argument for 'r' and 'r-sm' tags
- how to handle continuous guildline in UW passages + how to handle temporary/jump lines (draw p dashed pattern). Does it have to be done in .th2 or can we specify this in .th and automatically display it properly through layouts
- Github Actions and Therion: is there a use case for this? Maybe automatically update GIS whenever we commit new data.
- Legend symbols needs to be 'translated' to Slovenian/English combo as in Illustrator
- Test distox/topodroid data import. If you are using .py scripts, you need to clean up the data a bit. It will also produce station points at every splay
- Figure out how to best tackle the stitching of the scraps with adjacent area symbols of the same type. It produces a 'white line' at the junction. One way to solve this would be to use colour map-fg [100 0 0] in 'blue' for the whole map and just draw the dry sections white.