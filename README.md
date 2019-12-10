# HaloStatsParserProject
To parse the old xbox live halo game stats pages from halo.bungie.net archived by the ArchiveTeam into a usable json format.

## Goal
Set up a script so that you can download an archive from here: https://archive.org/details/archiveteam_halo, extract it, and have the script automatically parser all game stat pages from it and convert them into json files.

## Progress
- Main Script - WIP
- GameStatsHalo2.aspx - DONE
  - These archives do not seem to ever capture the total game medals tab, so the code will trigger an exception to alert the user if the script ever does actually come across one, but I don't think that will happen. Even if it did, I'm not sure if it's useful to capture total game medals in general, let alone for some insignificantly small amount of the billion games played.
- GameStatsHalo3.aspx - DONE
  - As far as I can tell, the files and viewer tabs were not captured by these archives because their contents do not load automatically with the page, so I believe this parsing grabs every single bit of information it can.
  - It seems like the game id parameter in these pages suffered an integer overflow or some other issue causing negative game ID's. I'm not aware of reference to the game's true ID within the page itself, so we will just have to go with what's in the url parameter.

## TODO
- Find every possible game stat page. ODST? 4? Reach? How far does these archive capture?
- Should I parse Halo 3 files? Users could capture screenshots and video clips which seem to be archived too, but I'm nont sure if I can easily map them to their metadata.
- Do I parse user profiles? Are these game specific or do they span across all games?
- What else is worth parsing that is saved in this archives, so that they only have to be processed once?

## Other Information
- Originally this started out by just curling archive.org for game stats pages and incrementing the gameid counter up until there were no more games. After doing some tests I quickly realized doing this for both Halo 2 and Halo 3 would probably take about 10 years on my current hardware setup. Processing game files locally after downloading an extracting the huge warc files proves to be much faster, and potentially easier to distribute the processing amongst others, so that is why this parser is built around downloading a warc file, extracting the contents, and then running this script on that directory versus just dowloading each file directing from archive.org.
