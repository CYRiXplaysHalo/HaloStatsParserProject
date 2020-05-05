# HaloStatsParserProject
To parse the old xbox live halo game stats pages from halo.bungie.net archived by the ArchiveTeam into a usable json format.

## Goal
Set up a script so that you can download an archive from here: https://archive.org/details/archiveteam_halo, extract it, and have the script automatically parser all game stat pages from it and convert them into json files.

## Progress
I am running this script on warc files as I have time and uploaded the parsed version of each warc file to here: https://archive.org/details/halo-stats-parser-project-files
There are 846 warc files and in about a week I've done 6, so this will be a very timely process. Please reach out if you are interested in helping.

## How to use
- You want to first download an archive from https://archive.org/details/archiveteam_halo.
- After it is downloaded use warcat to extract the archive to a folder: https://github.com/chfoo/warcat.
- Once you have all of the raw files in a folder, update lines 15-21 in BungiePageFinder.py to reflect the right directories and files you want to process.
- Execute BungiePageFinder.py. This script takes a while to run. On my 8-year old rig it takes about a day. On my 3 year old laptop it takes about 8 hours.
- Once it comples you will have json files for each page it parsed in your respective output directories.

## Next Steps
- Make BungiePageFinder.py take in command line arguments
- Set up process to collect and archive output json files.

## Progress
- Main Script - DONE
- GameStatsHalo2.aspx - DONE
  - These archives do not seem to ever capture the total game medals tab, so the code will trigger an exception to alert the user if the script ever does actually come across one, but I don't think that will happen. Even if it did, I'm not sure if it's useful to capture total game medals in general, let alone for some insignificantly small amount of the billion games played.
- GameStatsHalo3.aspx - DONE
  - As far as I can tell, the files and viewer tabs were not captured by these archives because their contents do not load automatically with the page, so I believe this parsing grabs every single bit of information it can.
  - It seems like the game id parameter in these pages suffered an integer overflow or some other issue causing negative game ID's. I'm not aware of reference to the game's true ID within the page itself, so we will just have to go with what's in the url parameter.
- Halo3UserContentDetails.aspx - DONE
  - These pages contain metadata about user submitted files.
  - At this point I'm not sure they link to the actual images/videos themselves, but they contain things like title, description, views, and ratings.
- odstg.aspx - DONE
  - I'll admit I stopped player the Halo series after Halo 3, so correct me if I'm wrong here but it seems like these pages only tracked ODST campaign games (single player, and co-op). The archive did not capture the silveright content, so these pages pretty much only contain who played, what map they played, how long they played for, and what difficulty they were on.
  
## TODO
- Do I parse user profiles? Are these game specific or do they span across all games?
- What else is worth parsing that is saved in this archives, so that they only have to be processed once?

## Other Information
- Originally this started out by just curling archive.org for game stats pages and incrementing the gameid counter up until there were no more games. After doing some tests I quickly realized doing this for both Halo 2 and Halo 3 would probably take about 10 years on my current hardware setup. Processing game files locally after downloading an extracting the huge warc files proves to be much faster, and potentially easier to distribute the processing amongst others, so that is why this parser is built around downloading a warc file, extracting the contents, and then running this script on that directory versus just dowloading each file directing from archive.org.
- This archive seems to have every Halo 2 game played on xbox live (that had it's game uploaded to halo.bungie.net). With Halo 3 I'm not so sure, but if I had to guess I would still say at least 90% of the games were captured in this archive.
