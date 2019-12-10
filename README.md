# HaloStatsParserProject
To parse the old xbox live halo game stats pages from halo.bungie.net archived by the ArchiveTeam into a usable json format.

## Goal
Set up a script so that you can download an archive from here: https://archive.org/details/archiveteam_halo, extract it, and have the script automatically parser all game stat pages from it and convert them into json files.

## Progress
- Main Script - WIP
- GameStatsHalo2.aspx - DONE
- GameStatsHalo3.aspx - DONE

## TODO
- Find every possible game stat page. ODST? 4? Reach? How far does these archive capture?
- Should I parse Halo 3 files? Users could capture screenshots and video clips which seem to be archived too, but I'm nont sure if I can easily map them to their metadata.
- Do I parse user profiles? Are these game specific or do they span across all games?
- What else is worth parsing that is saved in this archives, so that they only have to be processed once?
