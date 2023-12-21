#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import get_imdb_data as imdb
#from resources.libs import Open_Url, getmatch, makebuffer
#from resources.urls import urls
debug = False

#url_to_open = urls['nr'] #'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
#url_to_open = 'https://raw.githubusercontent.com/tombebbs1/MagicDragonKodi18/main/newreleases1.xml'
#HTML2 = Open_Url(url_to_open)

import requests
_url = 'https://raw.githubusercontent.com/tombebbs1/MagicDragonKodi18/main/newreleases1.xml'
response = requests.get(_url)
#print(response.content)
HTML2 = response.content.decode("utf8")
match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
text_file = 'data/match.txt'


#print(match2)

def get_data(what):
    urls = []
    #pattern = re.compile(r'https?://(www\.)?(\w+)(\-\w+)*(\.\w+)*/(\w+)(\.\w+)*(/(\w+)(\.\w+)*)*')
    pattern = re.compile(r'https?://[^:\'<]*[\.\w+]*')
    with open(text_file, 'r',encoding='utf8') as f:
        mylist = f.read().split("')")
    for item in mylist:
        url=[]
        if what.lower() in item.lower():
            #print(item.split(',')[0].replace('"','\''))
            title = item.split(',')[0].replace('"','\'').strip().replace('(\'[COLORwhite]','').replace('[/COLOR]\'','')
            #.replace('("[COLORwhite]','').replace('[/COLOR]\"','')
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
    new = False
    buffer='<style>body {font-family: sans-serif;} .float {float:left; width:200px; margin:1em 0;}'
    buffer+='.synop {height:300px;font-size: 12px;border:dotted;margin-left:1px; margin-right:1px;padding-top: 10px; padding-right: 15px;}ul {padding-inline-end: 15px;padding-inline-start: 27px;}'
    buffer+='#title{text-align:right;font-weight:bolder;text-decoration: underline;}'
    buffer+='</style>'
    #print(urls)
    
    #<img onmouseover="bigImg(this)" onmouseout="normalImg(this)" border="0" src="smiley.gif" alt="Smiley" width="32" height="32">

    #buffer+='<script>function bigImg(x) {x.style.height = "64px";  x.style.width = "64px";} '
    buffer+='<script>function bigImg(x) {x.style.width = "50%";} '
    #buffer+='function normalImg(x) {x.style.width = "100%";} '
    buffer+='function show(x) {console.log(x);document.getElementById("synop").innerHTML=x;}</script>'
    #buffer+='<style>img {width: 200px;height: 300px;}</style>'
    #buffer+='<style>div {position:relative;float:left;width:20%;margin:0 auto;}</style>'
    i=0
    for title,url in urls:
        #if i<5:print(title)
        if 'NEW RELEASES' not in title and title not in no_synop:  
            print(' -',title)
            try:
                synopsis = '<li>'+'<li>'.join(mydict[title].split('\n'))
                print(synopsis)                    
                buffer += '<div class="float"><a href="'+url[1]
                #buffer+='"><img onmouseover="'+synopsis+'" width="100%" src="'+url[-2]+'"/></a></div>'
                buffer+='"><img width="100%" src="'+url[-2]+'"/></a><div class="synop"><div id="title">'+ str(i+1)+' '+ title[:35] +'</div><ul>'+synopsis+'</ul></div></div>'
                #print(buffer)
                i+=1
            except:
                try:
                    s = imdb.get_summary(title)
                    synopsis = '<li>'+'<li>'.join(s.split('\n'))
                    mydict[title] = s
                    new = True                
                    print(synopsis)                    
                    buffer += '<div class="float"><a href="'+url[1]
                    #buffer+='"><img onmouseover="'+synopsis+'" width="100%" src="'+url[-2]+'"/></a></div>'
                    buffer+='"><img width="100%" src="'+url[-2]+'"/></a><div class="synop"><div id="title">'+ str(i+1)+' '+ title[:35] +'</div><ul>'+synopsis+'</ul></div></div>'
                    #print(buffer)
                    i+=1
                except:
                    pass
    if new :
        save_dict(mydict)
        
    buffer+='<br><p id="synop"></p>'
    #print(buffer)
    with open('html/found.html', 'w',encoding='utf8') as f:
        f.write(buffer)
    print('\n>>>>> Save in file:/home/pi/Documents/Python/streaming/html/found.html')
           
import json

def save_dict(_dict):
    #from resources.libs import save2file, read_json, read_pkl
    json_file = 'data/summaries.json'
    a_file = open(json_file, "w",encoding='utf8')
    json.dump(_dict, a_file)
    a_file.close()

def load_json():
    with open("data/summaries.json",encoding='utf8') as json_file:
        _mydict = json.load(json_file)
        #print("load_json",_mydict)
    return _mydict

def make_summary_dict(new=False):
    if new:
        # new dictionary
        _mydict={}
    else:
        with open("data/summaries.json",encoding='utf8') as json_file:
            _mydict = json.load(json_file)
            #print(mydict)
    first = True  # print the last updated title
    
    for k in match2: #[5:-1]:
        #print(k)
        if '<sublink>' in k[1] and 'COLORwhite' in k[0]:
            #print(k)
            
            title = k[0].split('[COLORwhite]',1)[1].split('[/COLOR]',1)[0]
            
            if debug : print(title)
            if '(' in title:
                year = '('+title.split('(',1)[1].split(')',1)[0]+')'
                title = title.split('(',1)[0].split(': ',1)[0] + year
            if first:
                print('Last title updated :',title)
                first = False
            
            if title not in _mydict.keys() and title not in no_synop:               
                try:
                    old = title
                    if ' (' not in title:
                        title = title.replace('(', ' (')
                        print(title)
                    summary = imdb.get_summary(title.lower())
                    print('\nnew : ',title)
                    print(summary,'\n')                
                    _mydict[old] = summary                    
                    new = True
                except:
                    print('No synopsis found for ',title)
    
    if new:
        print('Saving new dict')
        save_dict(_mydict)
    return _mydict

def get_dict():
    with open("data/summaries.json",encoding='utf8') as json_file:
        _mydict = json.load(json_file)
        return _mydict

def get_synopsis(title):
    return imdb.get_summary(title.lower())

def list_synopsis(_mydict,debug=False):
    buffer=''
    for k in _mydict.keys():
        if debug:
            print(k, '\n', _mydict[k], '\n')
        buffer += '\n'+k+ '\n'+ _mydict[k]+ '\n'
    with open('data/synopsis.txt','w',encoding='utf8') as f:
        f.write(buffer)


def find_synopsis(_mydict, what):
    found = 'Not in database'
    for k in _mydict.keys():
        if what.lower() in k.lower():
            print('Found: ',k, _mydict[k],'\n')
            found=k
    return found

def replace_synopsis(what,by):
    mydict.pop(what)
    summary = imdb.get_summary(by.lower())
    mydict[what] = summary

def verify(_mydict, whatkey):
    local = find_synopsis(_mydict, whatkey)
    distant = imdb.get_summary(whatkey.lower())
    print(local,'\n',distant)

no_synop= ["American Gangster Presents Big Fifty The Delronda Hood Story (2021)",
    "The Power of the Dog (2021) Screener",
    "Dogface: A Trap House Horror (2021)",
    "South Park: Post Covid: The Return of Covid (2021)",
    "Venom: Let There Be Carnage (2021) Watermarked HD 14/11",
    "Signed",
    "Rise and Shine",
    "Dear Evan Hansen (2021) Screener",
    "The Card Counter (2021) Screener",
    "star-crossed: the film (2021)",
    "The Guilty (2021) Screener",
    "Harry and Meghan: Escaping the Palace (2021)",
    "Dragon(2022)",
    "Alien(2021)",
    "Trapped By My Sugar Daddy (2022)",
    "Vanished(2022)",
    "Munich(2021)",
    "My Babysitter the Superhero (2022)",
    "Cinderella and the Little Sorcerer (2021)",
    "Every Last Secret (2022)",
    "The Nanny's Night (2022)",
    "A Royal Seaside Romance (2022)",
    "Minions and More Volume 1 (2022)",
    "Ivy and Bean (2022)",
    "The Curse of Wolf Mountain (2022)",
    "Oscars Handmade Halloween (2023)",
    "Living Next to Danger (2023)",
    "The Curse of Wolf Mountain (2022)",
    "I’ll Be Watching (2023)",
    "Her Fiance's Double Life (2023)",
    "Don't F**k in the Woods 2 (2022)",
    "It’s Beginning to Look a Lot Like Murder (2022)",
    "TÁR (2022)",
    "Hanuman Shadow Master (2022)",
    "Cider and Sunsets (2022)",
    "Bosch and Rockit (2022)",
    "Iké Boys (2022)",
    "Girls from Dubai (2021)"]

no_synop = ['Venom: Let There Be Carnage (2021) Watermarked HD 14/11',
            'Signed','Rise and Shine','Dear Evan Hansen (2021) Screener',
            'The Card Counter (2021) Screener','star-crossed: the film (2021)',
            'The Guilty (2021) Screener','Harry and Meghan: Escaping the Palace (2021)',
            'Dragon(2022)','Alien(2021)','Trapped By My Sugar Daddy (2022)','Vanished(2022)',
            'Munich(2021)','My Babysitter the Superhero (2022)','Cinderella and the Little Sorcerer (2021)',
            'Every Last Secret (2022)','The Nanny’s Night (2022)',
            'A Royal Seaside Romance (2022)','Minions and More Volume 1 (2022)',
            'Ivy and Bean (2022)','The Curse of Wolf Mountain (2022)','Oscars Handmade Halloween (2023)',
            'Living Next to Danger (2023)','The Curse of Wolf Mountain (2022)','I’ll Be Watching (2023)',
            'Her Fiance’s Double Life (2023)',"Don't F**k in the Woods 2 (2022)",'It’s Beginning to Look a Lot Like Murder (2022)',
            'TÁR (2022)','Hanuman Shadow Master (2022)','Cider and Sunsets (2022)','Bosch and Rockit (2022)',
            'Iké Boys (2022)','Girls from Dubai (2021)']

#no_synop = []

    
# add missing synopsis
def add_missing(_mydict):
    missing = {'Venom(2021)':'Synopsis : Eddie Brock attempts to reignite his career by interviewing serial killer Cletus Kasady, who becomes the host of the symbiote Carnage and escapes prison after a failed execution.\nDirector:Andy Serkis\nStars:Tom Hardy, Woody Harrelson, Michelle Williams, Naomie Harris',
           'Hacker(2022)':'Synopsis : Hackers are blamed for making a virus that will capsize five oil tankers.\nDirector:Iain Softley\nStars:Jonny Lee Miller, Angelina Jolie, Jesse Bradford, Matthew Lillard',
           'Montford(2021)':'Synopsis : A remarkable story inspired by the life of renowned Chickasaw cattleman Montford T. Johnson, a man who overcame great hardships to establish a ranching empire along the famous cattle highway of the American West, the Chisolm Trail.\nDirector:Nathan Frankowski\nStars:Martin Sensmeier, Dermot Mulroney, Tommy Flanagan, James Landry Hébert',
           'Dogface(2021)':'Synopsis : After moving into a haunted trap house, a troubled young hustler from the streets begins to discover his true purpose.\nDirector:Felix Jordan\nStars:Know Cash, Abms Daisy, Garron Gates, Gotti',
           'Myth(2021)': "Synopsis : An unfathomable incident introduces a genius engineer to dangerous secrets of the world, and to a woman from the future who's come looking for him.\nStars:\nPark Shin-Hye, In-ho Tae, Halley Kim",
           'Diana(2021)':'Synopsis : During the last two years of her life, Princess Diana embarks on a final rite of passage: a secret love affair with Pakistani heart surgeon Hasnat Khan.\nDirector:Oliver Hirschbiegel\nStars:Naomi Watts, Naveen Andrews, Cas Anvar, Charles Edwards',
           'star-crossed(2021)':'Synopsis : About an epic romance between a human girl and an alien boy when he and others of his kind are integrated into a suburban high school 10 years after they landed on Earth and were consigned to an internment camp.\nStars:\nMatt Lanter, Grey Damon, Greg Finley',
           'Journey of My Heart (2021)':"Synopsis : Unusually gifted, successful CEO/entrepreneur Sebastien Martin has experienced accurate prophetic visions for years. While ignoring his psychic abilities to build a normal life, Sebastien's\nDirector:Cybela Clare\nStar:Sebastien Martin",
           'VHS 94 (2021)':'Synopsis : A police S.W.A.T. team investigates about a mysterious VHS tape and discovers a sinister cult that has pre-recorded material which uncovers a nightmarish conspiracy.\nDirectors:Simon Barrett,\nChloe Okuno, Ryan Prows, Jennifer Reeder, Timo Tjahjanto|     Stars:Anna Hopkins, Christian Potenza, Brian Paul, Tim Campbell',
           'If I Cant Have Love I Want Power (2021)':"Synopsis : The music of Halsey's upcoming album, introduces a young pregnant Queen, Lila, as she wrestles with the chokehold of love to ultimately discover that the ability to create life (and end it) unlocks the paranormal power within her.\nDirector:Colin Tilley\nStars:Halsey, Sasha Lane, Vuk Celebic, Brian Caspe"
            }
    _mydict = {**_mydict, **missing}  # concatenate 2 dictionaries 
    # add by key
    _mydict['The Worst Person in the World (2021) Subbed']='Synopsis : The chronicles of four years in the life of Julie, a young woman who navigates the troubled waters of her love life and struggles to find her career path, leading her to take a realistic look at who she really is.\nDirector:Joachim Trier\nStars:Renate Reinsve, Anders Danielsen Lie, Maria Grazia Di Meo, Mia McGovern Zaini'
    _mydict['Vanished(2022)']="Synopsis : Story of a husband and wife that will stop at nothing to find their missing daughter, who disappeared on a family camping trip. When the police don't catch any leads, the duo take over.\nDirector:Peter Facinelli\nStars:Anne Heche, Thomas Jane, Jason Patric, Alex Haydon"
    _mydict['Munich(2021)']='Synopsis : A British diplomat travels to Munich in the run-up to World War II, where a former classmate of his from Oxford is also en route, but is working for the German government.\nDirector:Christian Schwochow\nStars:George MacKay, Jannis Niewöhner, Jeremy Irons, Liv Lisa Fries'
    _mydict['Alien(2021)']='Synopsis : A crash-landed alien named Harry who takes on the identity of a small-town Colorado doctor and slowly begins to wrestle with the moral dilemma of his secret mission on Earth.\nStars:\nSara Tomko, Elizabeth Bowen, Corey Reynolds'
    _mydict['Catwoman(2022)']='Synopsis : A shy woman, endowed with the speed, reflexes, and senses of a cat, walks a thin line between criminal and hero, even as a detective doggedly pursues her, fascinated by both of her personas.\nDirector:Pitof\nStars:Halle Berry, Sharon Stone, Benjamin Bratt, Lambert Wilson'
    _mydict['Dracula(2022)']="Synopsis : The centuries old vampire Count Dracula comes to England to seduce his barrister Jonathan Harker's fiancée Mina Murray and inflict havoc in the foreign land.\nDirector:Francis Ford Coppola\nStars:Gary Oldman, Winona Ryder, Anthony Hopkins, Keanu Reeves"
    _mydict['Pinocchio(2022)']='Synopsis : Young Pinocchio runs away from his genius creator Jepetto accompanied by the horse Tibalt to see the world and joins the traveling circus run by hustler Modjafocco.\nDirector:Vasiliy Rovenskiy\nStars:Jon Heder, Pauly Shore, Tom Kenny, Dmitriy Iosifov'
    # get value with key1 and save with key2
    key1 = 'Spider-Man : no way home (2021)'
    value = get_synopsis(key1)
    key2 = 'Spider-Man(2021)'
    _mydict[key2]= value
    
    # save to file
    save_dict(_mydict)

def add_new_key(_mydict):
    # get value with key1 and save with key2
    key1 = 'Spider-Man : no way home (2021)'
    value = get_synopsis(key1)
    key2 = 'Spider-Man(2021)'
    _mydict[key2]= value
    
def build(what):
    #list_synopsis(mydict)
    #what = 'kill'
    #replace_synopsis('Parallel  (2020)', 'Parallel  (2018)')
    ret = get_data(what)
    print('\nSearching for :',what)
    print('Found',len(ret),'titles :\n')
    make_page(ret)

def test():
    # find_synopsis(mydict, what)
    # whatkey='Midnight in the Switchgrass  (2021)'
    # verify(mydict, whatkey)
    '''
    for k in range(8,25):
        print(match2[k][0].split('e]')[1].split('[/C')[0])
        
    '''

    #key = ''
    #value = ""
    #add_missing(mydict,key,value)
    
    #replace_synopsis('Parallel  (2020)', 'Parallel  (2018)')


# create dictionary from file
if __name__ == '__main__':
    #pass
    mydict = make_summary_dict()

    #what = 'day'
    #build(what)

    # search for a film
    #find_synopsis(mydict,'burn')
    #find_synopsis(mydict,'deus')
