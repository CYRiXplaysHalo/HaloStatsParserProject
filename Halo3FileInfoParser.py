from lxml import etree
from bs4 import BeautifulSoup
import json
import urllib.request
import time

##with open('D:\HaloStats\onlinelinks2.txt') as f:
##    content = f.readlines()
##
##files = [x.strip() for x in content]

def parseHalo3FileInfoPage(filepath, output_dir):

    #print(filepath)
    game_id = filepath
    with open(str(game_id), "r", encoding="utf8") as myfile:
        h3_file_page=myfile.read().replace("\n", "")

    if h3_file_page.find('Unable to locate specified Halo 3 file. The file may not exist, or the system may have encountered an error.') < 0:
        if h3_file_page.find('filmclips') > 0:
            file_type = 'Film'
        else:
            file_type = 'Image'
        title = h3_file_page[h3_file_page.find('<div class="shareLeftHeader">')+29:]
        title = title[:title.find('<span>')].replace('&quot;','').strip()
        author = h3_file_page[h3_file_page.find('ctl00_mainContent_fileAuthorLink'):]
        author = author[author.find('>')+1:]
        date = author[author.find('on')+2:]
        author = author[:author.find('<')]
        date = date[:date.find('</span>')].strip()
        if date.find('on') > 0:
            date = date[date.find('on')+2:].strip()
        ssid = h3_file_page[h3_file_page.find('ssid=')+5:]
        ssid = ssid[:ssid.find('"')]
        info = h3_file_page[h3_file_page.find('shareMoreInfo">')+15:]
        info = info[:info.find('</div>')]
        ratings = h3_file_page[h3_file_page.find('ctl00_mainContent_ratingCountLabel')+36:]
        if 'downloads' in h3_file_page:
            downloads = ratings[:ratings.find('downloads')]
            downloads = downloads[downloads.find('-')+1:].replace('&nbsp;','')
        else:
            downloads = 0
        ratings = ratings[:ratings.find(' rating')].strip()
        ratings = ratings[ratings.rfind('>')+1:]
        
        file_details = h3_file_page[h3_file_page.find('File Details:'):]
        file_details = file_details[file_details.find("<ul>"):]
        file_details = file_details[:file_details.find("</ul>")+5]

        soup = BeautifulSoup(file_details, features="lxml")
        rows = soup.find_all('li')

        file_details_list = []
        for row in rows:
            cols = row.find_all('span')
            cols = [ele.text.strip() for ele in cols]
            if cols != []:
                name = cols[0][:cols[0].find(':')]
                value = cols[0][cols[0].find(':')+1:].replace('\t','')
                file_details_list.append({'name':name,'value':value})

        if '</a>' in date:
            date = date[date.find('on')+2:].replace('\t','').strip()

        if 'CTYPE' in ssid:
            ssid = ""
        
        game_id = game_id[game_id.find('id=')+3:]
        #print(game_id + "," +  title + "," + author + "," + date + "," + ssid + "," + ratings + "," + str(downloads) + "," + info)
        
##        if info == None and ssid == None:
##            output_json = {'h3fileid':game_id,'type':file_type,'title':title,'author':author,'date':date,'ratings':ratings,'dl':downloads,'file_details':file_details_list}
##        elif info == None and ssid != None:
##            output_json = {'h3fileid':game_id,'type':file_type,'title':title,'author':author,'date':date,'ratings':ratings,'dl':downloads,'file_details':file_details_list}
##        elif info != None and ssid == None:
##            output_json = {'h3fileid':game_id,'type':file_type,'ssid':ssid,'title':title,'author':author,'date':date,'ratings':ratings,'dl':downloads,'file_details':file_details_list,'info':info}
##        else:
        output_json = {'h3fileid':game_id,'type':file_type,'ssid':ssid,'title':title,'author':author,'date':date,'ratings':ratings,'dl':downloads,'file_details':file_details_list,'info':info}
        
        with open(output_dir + str(game_id) + '.json', 'w') as fp:
            json.dump(output_json, fp)
