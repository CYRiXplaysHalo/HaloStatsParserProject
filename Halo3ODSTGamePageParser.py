from lxml import etree
from bs4 import BeautifulSoup
import json
import urllib.request
import time

##with open('D:\HaloStats\odstlinks.txt') as f:
##    content = f.readlines()
##
##files = [x.strip() for x in content] 

def parseHalo3ODSTGame(filepath, output_dir):

    #print(filepath)
    game_id = filepath
    with open(str(game_id), "r", encoding="utf8") as myfile:
            odst_game_page=myfile.read().replace("\n", "")

    if odst_game_page.find('We\'re Sorry. Unfortunately, we don\'t have a record of this game or we have temporarily turned off game statistics.') < 0:
        game_type = odst_game_page[odst_game_page.find("ctl00_Head1"):]
        map_name = game_type[62:]
        date_time = map_name[map_name.find(": ")+2:]
        date_time = date_time[:date_time.find("</title>")]
        map_name = map_name[:map_name.find(" (")]
        game_type = game_type[game_type.find("(")+1:]
        game_type = game_type[:game_type.find(")")]
        total_length = odst_game_page[odst_game_page.find("Total Length: <span>")+20:]
        total_length = total_length[:total_length.find("</span>")]
        difficulty = odst_game_page[odst_game_page.find('ctl00_metaDescription'):]
        difficulty = difficulty[difficulty.find(date_time)+len(date_time) + 3:]
        difficulty = difficulty[:difficulty.find(' difficulty')]

        topfour = odst_game_page[odst_game_page.find("<div class=\"topfour\">"):]
        topfour = topfour[:topfour.find("<div class=\"detailinfo\">")]

        soup = BeautifulSoup(topfour, features="lxml")
        rows = soup.find_all("div", {"class": "wrapper"})

        player_stats_list = []
        for row in rows:
            cols = row.find_all("li")
            cols = [ele.text.strip() for ele in cols]
            emblem = str(row)[str(row).find('/Stats/emblem.ashx?')+19:]
            emblem = emblem[:emblem.find('"')].replace('&amp;','&')
            stats = {"name":cols[0],"tag":cols[1],"emblem":emblem,"points":cols[2],"kills":cols[3],"deaths":cols[0]}
            player_stats_list.append(stats)

        game_id = game_id[game_id.find('guid=')+5:]
        output_json = {"game_id":game_id, "type":game_type, "map":map_name, "datetime":date_time, "length":total_length, "difficulty":difficulty, "stats":player_stats_list}
        #print(game_id + "," + game_type + "," + map_name  + "," +  date_time  + "," + total_length  + "," + difficulty + "," + str(len(player_stats_list)))
        
        with open(output_dir + str(game_id) + '.json', 'w') as fp:
                json.dump(output_json, fp)
