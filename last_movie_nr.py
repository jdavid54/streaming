import re
import get_imdb_data as imdb
from resources.libs import Open_Url, getmatch, makebuffer

url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
HTML2 = Open_Url(url_to_open)
match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
text_file = 'data/match.txt'

    
def get_data(what):
    urls = []
    #pattern = re.compile(r'https?://(www\.)?(\w+)(\-\w+)*(\.\w+)*/(\w+)(\.\w+)*(/(\w+)(\.\w+)*)*')
    pattern = re.compile(r'https?://[^:\'<]*[\.\w+]*')
    with open(text_file, 'r') as f:
        mylist = f.read().split("')")
    for item in mylist:
        url=[]
        if what.lower() in item.lower():
            #print(item.split(',')[0].replace('"','\''))
            title = item.split(',')[0].replace('"','\'').strip().replace('(\'[COLORwhite]','').replace('[/COLOR]\'','')#.replace('("[COLORwhite]','').replace('[/COLOR]\"','')
            #print(title)
            subbed_urls = pattern.finditer(item)
            for m in subbed_urls:
                #print('*',m.group())
                url.append(m.group())
            if url!=[]:
                urls.append((title,url))
    return urls   #urls[0][1],urls[0][-2] = link to streaming page and picture   
    # urls : list of(title + list of urls)

def make_page(urls):
    buffer='<style>.float {float:left; width:20%; margin:1em 0;}</style>'
    #buffer+='<style>img {width: 200px;height: 300px;}</style>'
    #buffer+='<style>div {position:relative;float:left;width:20%;margin:0 auto;}</style>'
    for i,(title,url) in enumerate(urls):
        buffer += '<div class="float">' + str(i+1)+' '+ title[:35] +'<br><a href="'+url[1]+'"><img width="100%" src="'+url[-2]+'"/></a></div>'
    #print(buffer)
    with open('html/found.html', 'w') as f:
        f.write(buffer)
    print('file:/home/pi/Documents/Python/streaming/html/found.html')
           

import json

def save_dict(mydict):
    #from resources.libs import save2file, read_json, read_pkl
    json_file = 'data/summaries.json'
    a_file = open(json_file, "w")
    json.dump(mydict, a_file)
    a_file.close()

def load_json():
    with open("data/summaries.json") as json_file:
        mydict = json.load(json_file)
        print(mydict)

def make_summary_dict(new=False):
    if new:
        # new dictionary
        mydict={}
    else:
        with open("data/summaries.json") as json_file:
            mydict = json.load(json_file)
            #print(mydict)
    for k in match2:
        if 'ignorme' not in k:
            title = k[0].split('[COLORwhite]',1)[1].split('[/COLOR]',1)[0]
            year = '('+title.split('(',1)[1].split(')',1)[0]+')'
            title = title.split('(',1)[0].split(': ',1)[0] + ' ' + year

            if title not in mydict.keys():               
                try:
                    print('new : ',title)
                    summary = imdb.get_summary(title.lower())[1]
                    print(summary,'\n')                
                    mydict[title] = summary
                    new = True
                except:
                    print('No synopsis found for ',title)
    
    if new:
        print('Saving')
        save_dict(mydict)
    return mydict

def list_synopsis(mydict):
    buffer=''
    for k in mydict.keys():
        print(k, '\n', mydict[k], '\n')
        buffer += '\n'+k+ '\n'+ mydict[k]+ '\n'
    with open('data/synopsis.txt','w') as f:
        f.write(buffer)


def find_synopsis(mydict, what):
    for k in mydict.keys():
        if what.lower() in k.lower():
            print('Found: ',k, mydict[k],'\n')

def replace_synopsis(what,by):
    mydict.pop(what)
    summary = imdb.get_summary(by.lower())[1]
    mydict[what] = summary

def verify(mydict, whatkey):
    local = find_synopsis(mydict, whatkey)
    distant = imdb.get_summary(whatkey.lower())[1]
    print(local,'\n',distant)

mydict = make_summary_dict()

#list_synopsis(mydict)
what = 'snake'
#replace_synopsis('Parallel  (2020)', 'Parallel  (2018)')

urls = get_data(what)
make_page(urls)
print()
# find_synopsis(mydict, what)
# whatkey='Midnight in the Switchgrass  (2021)'
# verify(mydict, whatkey)