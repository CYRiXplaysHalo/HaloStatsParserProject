import glob
from lxml import etree
from bs4 import BeautifulSoup
import json
import urllib.request
import time
import Halo3GamePageParser
import Halo2GamePageParser
import Halo3ODSTGamePageParser
import Halo3FileInfoParser
from datetime import datetime
import os


working_dir = 'D:\HaloStats\\'
halo3_game_output_dir = 'D:\HaloStats\GameStats3\\'
halo2_game_output_dir = 'D:\HaloStats\GameStats2\\'
halo3odst_game_output_dir = 'D:\HaloStats\GameStatsODST\\'
halo3_info_output_dir = r"D:\HaloStats\UserContent3\\"
warc_dump_dir = 'D:\HaloStats\halo_20141105063210'
warc_archive_name = 'D:\HaloStats\halo_20141105063210.megawarc.warc.gz'

##extract_command = "python -m warcat extract " + warc_archive_name + " --output-dir " + warc_dump_dir + " --progress"
##os.system("mkdir " + warc_dump_dir)
##os.system(extract_command)

print("Finding Halo 3 games... " + str(datetime.time(datetime.now())))
halo3files = glob.glob(warc_dump_dir + "\halo.bungie.net\Stats\GameStatsHalo3.aspx*")
print("All Halo 3 games found. There are " + str(len(halo3files)) + " Halo 3 Game Files. " + str(datetime.time(datetime.now())))

with open(working_dir + "h3gameids.txt", 'a') as f:
    for item in halo3files:
        f.write("%s\n" % item)

print("Parsing Halo 3 Game Stat Pages... " + str(datetime.time(datetime.now())))

h3_counter = 0
for halo3game in halo3files:
    if h3_counter % 1000 == 0:
        print(str(h3_counter) + "/" + str(len(halo3files)) + " complete. " + str(h3_counter/len(halo3files)))
    Halo3GamePageParser.parseHalo3Game(halo3game, halo3_game_output_dir, working_dir)
    h3_counter += 1

print("Parsing complete. " + str(datetime.time(datetime.now())))

print("Finding Halo 2 games... " + str(datetime.time(datetime.now())))
halo2files = glob.glob(warc_dump_dir + "\halo.bungie.net\Stats\GameStatsHalo2.aspx*")
print("All Halo 2 games found. There are " + str(len(halo2files)) + " Halo 2 Game Files. " + str(datetime.time(datetime.now())))

with open(working_dir + "h2gameids.txt", 'a') as f:
    for item in halo2files:
        f.write("%s\n" % item)

print("Parsing Halo 2 Game Stat Pages... " + str(datetime.time(datetime.now())))

h2_counter = 0
for halo2game in halo2files:
    if h3_counter % 1000 == 0:
        print(h2_counter + "/" + str(len(halo2files)) + " complete. " + str(h2_counter/len(halo2files)))
    Halo2GamePageParser.parseHalo2Game(halo2game, halo2_game_output_dir, working_dir)
    h2_counter += 1

print("Parsing complete. " + str(datetime.time(datetime.now())))

print("Finding Halo 3 ODST games... " + str(datetime.time(datetime.now())))
halo3odstfiles = glob.glob(warc_dump_dir + "\halo.bungie.net\Stats\odstg.asp*")
print("All Halo 3 ODST games found. There are " + str(len(halo3odstfiles)) + " Halo 3 ODST Game Files. " + str(datetime.time(datetime.now())))

with open(working_dir + "h3odstgameids.txt", 'a') as f:
    for item in halo3odstfiles:
        f.write("%s\n" % item)

print("Parsing Halo 3 ODST Game Stat Pages... " + str(datetime.time(datetime.now())))

h3odst_counter = 0
for halo3odstgame in halo3odstfiles:
    if h3odst_counter % 1000 == 0:
        print(str(h3odst_counter) + "/" + str(len(halo3odstfiles)) + " complete. " + str(h3odst_counter/len(halo3odstfiles)))
    Halo3ODSTGamePageParser.parseHalo3ODSTGame(halo3odstgame, halo3odst_game_output_dir)
    h3odst_counter += 1

print("Parsing complete. " + str(datetime.time(datetime.now())))

print("Finding Halo 3 User Content Info...")
halo3infofiles = glob.glob(warc_dump_dir + "\halo.bungie.net\Online\Halo3UserContentDetails.aspx*")
print("All Halo 3 User Content Info Pages found. There are " + str(len(halo3infofiles)) + " Halo 3 User Content Info Pages.")

with open(working_dir + "h3infoids.txt", 'a') as f:
    for item in halo3infofiles:
        f.write("%s\n" % item)

print("Parsing Halo 3 User Content Info Pages...")

h3info_counter = 0
for halo3infogame in halo3infofiles:
    if h3info_counter % 1000 == 0:
        print(str(h3info_counter) + "/" + str(len(halo3infofiles)) + " complete. " + str(h3info_counter/len(halo3infofiles)))
    Halo3FileInfoParser.parseHalo3FileInfoPage(halo3infogame, halo3_info_output_dir)
    h3info_counter += 1

print("Parsing complete.")

##files = glob.glob('D:\HaloStats\warc_dump\halo.bungie.net\Stats\GameStatsHalo2.aspx*')
##
##with open('D:\HaloStats\h2gameids.txt', 'w') as f:
##    for item in files:
##        f.write("%s\n" % item)

##files = glob.glob('D:\HaloStats\warc_dump_halo_20141107084942\halo.bungie.net\Online\*')
##
##
##with open('D:\\HaloStats\\allonlinelinks2.txt', 'a') as f:
##    for item in files:
##        f.write("%s\n" % item)
