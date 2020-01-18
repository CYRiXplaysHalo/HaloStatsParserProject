import glob
from lxml import etree
from bs4 import BeautifulSoup
import json
import urllib.request
import time



##with open('D:\HaloStats\h3gameids.txt') as f:
##    content = f.readlines()
##
##files = [x.strip() for x in content] 

def parseHalo3Game(filepath, output_dir, working_dir):
    game_id = filepath
    
    with open(game_id, 'r', encoding="utf8") as myfile:
        h3_game_page=myfile.read().replace('\n', '')

    if(h3_game_page.count('We\'re Sorry. Unfortunately, we don\'t have a record of this game or we have temporarily turned off game statistics.') > 0):
        #print("No data for this game :(")
        with open(working_dir + "h3_no_data_games.log", 'a') as myfile:
                myfile.write(str(game_id) + "\n")                 
    else:
        with open(working_dir + "h3_yes_data_games.log", 'a') as myfile:
                myfile.write(str(game_id) + "\n")      
            
        game_info = h3_game_page[h3_game_page.find('ctl00_mainContent_bnetpgd_pnlGameDetails'):]
        game_info = game_info[:game_info.find('<li></li>')]

        map_name = game_info[game_info.find('/images/Halo3Stats/Maps/largemaps/')+34:]
        map_name = map_name[:map_name.find('.jpg')]

        game_name = game_info[game_info.find('<li class="first styled">')+25:]
        game_name = game_name[:game_name.find(' on')]

        playlist = game_info[game_info.find('<li class="styled">Playlist - ')+30:]
        playlist = playlist[:playlist.find('</li>')].replace('&nbsp;','')

        datetime = game_info[game_info.find('<li>')+4:]
        datetime = datetime[:datetime.find('&nbsp;')]

        game_length = game_info[game_info.find('Length: ')+8:]
        game_length = game_length[:game_length.find('&nbsp;')]

        carnage_report = h3_game_page[h3_game_page.find('ctl00_mainContent_bnetpgd_pnlKills'):]
        carnage_report = carnage_report[:carnage_report.find("</table>")+8]
        carnage_report = carnage_report[carnage_report.find("<table"):]

        game_files_count = h3_game_page[h3_game_page.find('Game Files (')+12:]
        game_files_count = game_files_count[:game_files_count.find(")")]
        game_files_count = int(game_files_count)

        if h3_game_page.find('Screens Files (') > 0:
            screens_files_count = h3_game_page[h3_game_page.find('Screens Files (')+12:]
            screens_files_count = screens_files_count[:screens_files_count.find(")")]
            screens_files_count = int(screens_files_count)
        else:
            screens_files_count = 0

        if h3_game_page.find('Clips Files (') > 0:
            clips_files_count = h3_game_page[h3_game_page.find('Clips Files (')+12:]
            clips_files_count = clips_files_count[:clips_files_count.find(")")]
            clips_files_count = int(clips_files_count)
        else:
            clips_files_count = 0
        
        soup = BeautifulSoup(carnage_report, features="lxml")
        carnage_report_list = []
        carnage_report_team_list = []
        carnage_report_emblem_list = []
        carnage_report_color_list = []
        carnage_report_progress_list = []

        total_game_medals = h3_game_page[h3_game_page.find('<div class="top_medals_cont">'):]
        total_game_medals = total_game_medals[:total_game_medals.find('<div id="ctl00_mainContent_bnetpgd_pnlFiles')]

        soup2 = BeautifulSoup(total_game_medals, features="lxml")
        rows2 = soup2.find_all("div", {"class": "medal"})
        total_game_medals_list = []
        for row in rows2:
            medal_count = str(row)[str(row).find('num')+5:]
            medal_count = medal_count[:medal_count.find('<')]

            medal_title = str(row)[str(row).find('title')+7:]
            medal_title = medal_title[:medal_title.find('<')]
            total_game_medals_list.append({'medal':medal_title,'count':medal_count})

        breakdown = h3_game_page[h3_game_page.find('<div id="ctl00_mainContent_bnetpgd_pnlBreakdown"'):]
        breakdown = breakdown[:breakdown.find('<div id="ctl00_mainContent_bnetpgd_pnlFieldStats')]
        breakdown = breakdown[breakdown.find('<table class="stats" style="width:868px;" cellspacing="0" cellpadding="0">'):]
        breakdown = breakdown[:breakdown.find('</table>')]
        
        soup3 = BeautifulSoup(breakdown, features="lxml")
        rows3 = soup3.find_all('tr')
        breakdown_list = []
        for row in rows3:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            name = cols[0]
            weapons = cols[1]
            melee = cols[2]
            grenades = cols[3]
            vehicle = cols[4]
            other = cols[5]
            twb = cols[6]
            twb_list = twb[31:].split(' Kill(s)')
            weapon_list = []
            for weapon in twb_list:
                weapon_name = weapon[:weapon.rfind(' ')].strip()
                weapon_count = weapon[weapon.rfind(' ')+1:].strip()
                if weapon_name != '':
                    weapon_list.append({'weapon':weapon_name,'count':weapon_count})

            if 'Team' in name:
                breakdown_list.append({'name':name,'weapons':weapons,'melee':melee,'grenades':grenades,'vehicle':vehicle,'other':other})
            else:
                breakdown_list.append({'name':name,'weapons':weapons,'melee':melee,'grenades':grenades,'vehicle':vehicle,'other':other,'total_weapon_breakdown':weapon_list})

        if len(breakdown_list) > 1:
            breakdown_list.pop(0) #first item is garbage
    
        field_stats = h3_game_page[h3_game_page.find('ctl00_mainContent_bnetpgd_pnlFieldStats'):]
        field_stats = field_stats[:field_stats.find('</table>')]
        field_stats = field_stats[field_stats.find('<table class="stats"'):]        

        soup4 = BeautifulSoup(field_stats, features="lxml")
        rows4 = soup4.find_all('tr')
        field_stats_list = []
        for row in rows4:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]

            name = cols[0]
            headshots = cols[1]
            best_spree = cols[2]
            avg_life = cols[3]
            medals = cols[4]

            mkb_table = str(row.find_all('td'))
            soup_mkb = BeautifulSoup(mkb_table, features="lxml")
            rows_mkb = soup_mkb.find_all("li", {'class':'vs_row'})

            mkb_list = []
            mka_list = []
            for mkb_row in rows_mkb:
                opponent = str(mkb_row)[str(mkb_row).find('vs_row_player')+15:]
                opponent = opponent[:opponent.find(':')].strip()

                kills = str(mkb_row)[str(mkb_row).find('vs_row_kills')+15:]
                kills = kills[:kills.find('</div>')].strip()

                if 'x' in kills:
                    mka_list.append({'opponent':opponent,'kills':kills.replace('x','').strip()})
                else:
                    mkb_list.append({'opponent':opponent,'kills':kills})

            if 'Team' in name:
                field_stats_list.append({'name':name,'headshots':headshots,'best_spree':best_spree,'avg_life':avg_life,'medals':medals})
            else:
                field_stats_list.append({'name':name,'headshots':headshots,'best_spree':best_spree,'avg_life':avg_life,'medals':medals,'most_kills':mkb_list,'most_killed_by':mka_list})

        if len(field_stats_list) > 1:
            field_stats_list.pop(0) #first element is garbage
        
        if 'guid' in game_id:
            game_id = game_id[game_id.find("guid=")+5:]
        else:
            game_id = game_id[game_id.find("gameid=")+7:game_id.find('&player')]
        
        rows = soup.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            #print(cols)
            if("Team" in str(row) or "Clan" in str(row)):
                team_list = [ele for ele in cols if ele]
                color = str(row)[str(row).find('background-color:')+17:]
                color = color[:color.find('"')]
                team_list.append(color.replace(';',''))
                carnage_report_team_list.append(team_list)
            else: 
                carnage_report_list.append([ele for ele in cols if ele])
            if("background-color" in str(row) and "Team" not in str(row) and "Clan" not in str(row)):
                #color = str(row)[str(row).find('play_matte'):]
                color = str(row)[str(row).find('ColorBG" style="background-color:')+33:]
                color = color[:color.find('"')]
                carnage_report_color_list.append(color.replace(';',''))
            if("/Stats/emblem.ashx" in str(row)):
                emblem = str(row)[str(row).find('/Stats/emblem')+19:]
                emblem = emblem[:emblem.find('"')]
                carnage_report_emblem_list.append(emblem.replace('&amp;','&'))
            if("width:40px;height:15px;" in str(row)):
                progress = str(row)[str(row).find('width:40px;height:15px;')+44:]
                progress = progress[:progress.find('px')]
                progress_percentage = int(progress)/40
                carnage_report_progress_list.append(progress_percentage)
        carnage_report_json = []
        
        for i in range(1,len(carnage_report_list)):
            if(carnage_report_list[i][0].rfind('\n') != -1):
                last_space = carnage_report_list[i][0].rfind('\n')
            else:
                last_space = carnage_report_list[i][0].rfind(' ')
            if(carnage_report_progress_list != []):
                player_rank = int(carnage_report_list[i][0][last_space+1:])
                player_name = carnage_report_list[i][0][:last_space].replace('\n','')
            else:
                player_name = carnage_report_list[i][0]
            if len(carnage_report_team_list) > 0:
                if len(carnage_report_progress_list) == len(carnage_report_color_list) and len(carnage_report_color_list) == (len(carnage_report_list)-1):
                    row = {'name':player_name,'team':carnage_report_color_list[i-1],'progress':carnage_report_progress_list[i-1],'emblem':carnage_report_emblem_list[i-1],'rank':player_rank,'kills':carnage_report_list[i][1],'assists':carnage_report_list[i][2],'deaths':carnage_report_list[i][3],'suicides':carnage_report_list[i][5],'betrayals':carnage_report_list[i][6],'score':carnage_report_list[i][7]}
                else:
                    row = {'name':player_name,'team':carnage_report_color_list[i-1],'emblem':carnage_report_emblem_list[i-1],'kills':carnage_report_list[i][1],'assists':carnage_report_list[i][2],'deaths':carnage_report_list[i][3],'suicides':carnage_report_list[i][5],'betrayals':carnage_report_list[i][6],'score':carnage_report_list[i][7]}
            else:
                if len(carnage_report_progress_list) == len(carnage_report_color_list) and len(carnage_report_color_list) == (len(carnage_report_list)-1):
                    row = {'name':player_name,'player_color':carnage_report_color_list[i-1],'progress':carnage_report_progress_list[i-1],'emblem':carnage_report_emblem_list[i-1],'rank':player_rank,'kills':carnage_report_list[i][1],'assists':carnage_report_list[i][2],'deaths':carnage_report_list[i][3],'suicides':carnage_report_list[i][5],'betrayals':carnage_report_list[i][6],'score':carnage_report_list[i][7]}
                else:
                    row = {'name':player_name,'player_color':carnage_report_color_list[i-1],'emblem':carnage_report_emblem_list[i-1],'kills':carnage_report_list[i][1],'assists':carnage_report_list[i][2],'deaths':carnage_report_list[i][3],'suicides':carnage_report_list[i][5],'betrayals':carnage_report_list[i][6],'score':carnage_report_list[i][7]}
            carnage_report_json.append(row)

        if len(carnage_report_team_list) > 0:
            team_stats = []
            for k in range(0,len(carnage_report_team_list)):
                team = carnage_report_team_list[k][0]
                kills = carnage_report_team_list[k][1]
                assists = carnage_report_team_list[k][2]
                deaths = carnage_report_team_list[k][3]
                suicides = carnage_report_team_list[k][5]
                betrayals = carnage_report_team_list[k][6]
                score = carnage_report_team_list[k][7]
                color = carnage_report_team_list[k][8].replace(';','')
                team_stats.append({'team':team,'kills':kills,'assists':assists,'deaths':deaths,'suicides':suicides,'betrayals':betrayals,'score':score,'color':color})
            game_json = {'gameId':game_id,'map':map_name,'game':game_name,'playlist':playlist,'dateTime':datetime,'length':game_length,'files':game_files_count,'screens':screens_files_count,'clips':clips_files_count,'total_medal_counts':total_game_medals_list,'field_stats':field_stats_list,'breakdowns':breakdown_list,'teamReports':team_stats,'carnageReport':carnage_report_json}
        else:
            game_json = {'gameId':game_id,'map':map_name,'game':game_name,'playlist':playlist,'dateTime':datetime,'length':game_length,'files':game_files_count,'screens':screens_files_count,'clips':clips_files_count,'total_medal_counts':total_game_medals_list,'field_stats':field_stats_list,'breakdowns':breakdown_list,'carnageReport':carnage_report_json}

        with open(output_dir + str(game_id) + '.json', 'w') as fp:
            json.dump(game_json, fp)
