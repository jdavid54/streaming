#-------------------------------------------------------------------------------
# Name:        libs.py
# Purpose:     load txt file, replace tags, css display
#
# Author:      Jean
# old : http://supremacy.org.uk/tombraider/dogsbollocks/
# Created:     19/04/2019
# Copyright:   (c) Jean 2019
# Licence:     Free Open Source
#-------------------------------------------------------------------------------
#import urllib
from urllib.request import urlopen, Request
import datetime
#import shutil
import re
#import os
#import time
import requests
#import _Edit
try:
    import json
except:
    import simplejson as json

import pickle

file_name = "data/data.json"
pkl1, pkl2 = 'data/initials.pkl', 'data/urls.pkl'
outfile = 'data/list_movies.txt'

# variables  : debug, initial, Search_name, Search_filter, data_file from makehtmlfile.py
style = '<html><head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'

def Open_Url(url):
    req = Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
    response = ''
    link = ''
    try:
        response = urlopen(req)
        link=response.read()
        if debug: print('OK reading url')
        response.close()
    except: pass
    if link != '':
        return link
    else:
        link = 'Opened'
        return link

def get_url(Search_name):
    Search_title = Search_name.lower().replace(' ','')
    try:
        if initial:
            for k,v in initials.items():
                if Search_title[0] in k:
                    return v
        else:
            return urls[Search_title]
    except:
        #default url if error in key
        return 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
    
def chooseURL(Search_name):
    Search_title = Search_name.lower().replace(' ','')
    if initial:      #if initial=True, search by initials
        if Search_title[0] in 'abcd':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/A-D.txt'
        elif Search_title[0] in 'efgh':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/E-H.txt'
        elif Search_title[0] in 'ijkl':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/I-L.txt'
        elif Search_title[0] in 'mnop':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/M-P.txt'
        elif Search_title[0] in 'qrs':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/Q-S.txt'
        elif Search_title[0] in 't':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/T.txt'
        elif Search_title[0] in 'uvwxyz':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/U-Z.txt'
        elif Search_title[0] in '0123456789':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/0-1000000.txt'
        elif Search_title[0] in '#':
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/realdebrid.txt'
    else:
        if Search_title == "nr":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
        if Search_title == "nr2":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/nr2.txt'
        if Search_title == "nr3":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/nr3.txt'
        if Search_title == "nr4":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/nr4.txt'
        if Search_title == "nr5":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/nr5.txt'
        if Search_title == "4k":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/uhd.txt'
        if Search_title == "cam":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/cams.txt'
        if Search_title == "box":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/boxsets.txt'
        if Search_title == "full":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/fullseries.txt'
        if Search_title == "special":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/specials.txt'
        if Search_title == "kids":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/kidsmovies.txt'
        if Search_title == "horror":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/horror.txt'
        if Search_title == "0-9":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/0-1000000.txt'
        if Search_title == "doc":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/documentaries.txt'
        if Search_title == "action":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10action.txt'
        if Search_title == "alien":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10alieninvasion.txt'
        if Search_title == "anim":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10animation.txt'
        if Search_title == "comedies":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10comedies.txt'
        if Search_title == "disaster":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10disaster.txt'
        if Search_title == "fight":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10fight.txt'
        if Search_title == "gangster":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10gangster.txt'
        if Search_title == "ghost":
            url_to_open = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/top10ghosthorror.txt'
    return url_to_open

def find_text(t,sub1,sub2=''):
    start=([m.start() for m in re.finditer(sub1, t)])
    if sub2 != '':
        end=([m.start()+4 for m in re.finditer(sub2, t)])
        return start, end
    return start

def appendHost(url):
    for i in ('vidoza', 'openload', 'streamango', 'uptobox', '1fichier', 'rapidgator',\
     'streamcherry', 'vidto', 'vidzi', 'streamcloud', 'youtube', 'veehd', 'youwatch', 'uptostream'):
        if i in url:
            url = url.replace('</a>',' ['+i.capitalize()+']</a>')
    return url

def modifyURL(url):
    if debug: print("modifying",url)
    u,v = find_text(url,'<a','</a')
    result=''
    for i in range(len(u)):
        try:
            url2=(url[u[i]:v[i]])
        except:
            url2=''
        if linkok(url2.lower()):
            result+=appendHost(url2)+'<br>'
        else:
            result+=appendHost(url2)+'-warning: dont use !<br>'
    return result

def getmatch(Search_name):
    #source = chooseURL(Search_name)
    source = get_url(Search_name)
    if debug: print(Search_name,source,Search_filter)
    print(Search_name,source)
    HTML2 = Open_Url(source)
    match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
#     if debug:
#         f= open("data/match2.txt","w+")
#         f.write(str(match2))
#         f.close()
    with open(data_file, 'w+') as filehandle:
        for listitem in match2:
            #print(listitem)
            filehandle.write('%s\n' % str(listitem))
    return match2

def linkok(link):
    test=True
    for sub in ('vidto','vidzi'):
        if link.find(sub) != -1:
            test=False
    return test

def render(url2, name2):
    # if multiple links
    if 'sublink' in url2:
        #rectify bad url
        index=url2.find('sublink')
        url2=url2[index:]
        #replace tags
        url2 = url2.replace('sublink:LISTSOURCE:','<a href="')
        url2 = url2.replace('ublink:LISTSOURCE:','<a href="')
        url2 = url2.replace('::LISTNAME:','" target="new">')
        url2 = url2.replace('::#','</a>')
        url2 = url2.replace('\\r\\n','<br>')
        url2 = url2.replace('[COLORgold]','')
        url2 = url2.replace('[COLORorchid][/COLOR]','Link to video')
        url2 = url2.replace('[COLORorchid]','')
        url2 = url2.replace('[COLORred]','')
        url2 = url2.replace('[COLORwhite]','')
        url2 = url2.replace('[/COLOR]','')
        url2 = modifyURL(url2)
        name2 = name2.replace('[COLOR white]','')
        name2 = name2.replace('[COLORwhite]','')
        name2 = name2.replace('[COLOR gold]','')
        name2 = name2.replace('[COLOR pink]','')
        name2 = name2.replace('[COLORred]','')
        name2 = name2.replace('[B]','')
        name2 = name2.replace('[/COLOR]','')
        name2 = name2.replace('[/I]','')
        name2 = name2.replace('[I]','')
        name2 = name2.replace('[/B]','')
    else:    #or only one link
        name2 = name2.replace('[COLORwhite]','')
        name2 = name2.replace('[/COLOR]','')
        name2 = name2.replace('[COLOR gold]','')
        name2 = name2.replace('[B]','')
        name2 = name2.replace('[/B]','')
        url2 = '<a href="'+url2+'">Link to video</a>'
        url2 = modifyURL(url2)
    return url2, name2
                
def makebuffer(match_file):
    FANART = 'fanart.jpg'
        
    #do_all = False
    if do_all:
        # make the whole page
        list_movies = []
    else:
        try:
            with open ('data/list_movies.txt', 'rb') as fp:
                list_movies = pickle.load(fp)
        except:
            list_movies = []
        
    # get old list
    with open("html/nr_vignette.html","r") as f:
        old_list = f.read().split('</h4>')[1]
    
    n=0                     # error image
    m=0                     # number of movies
    new = False
    buffer=style+'<body><h1>Free movies ! Enjoy ! </h1>'
    if Search_name != 'nr' :
        buffer+= '<a href="nr_vignette.html">Back page 1</a>'
    else:
        buffer+= '<a href="nr2_after_select.html">Page 2</a>&nbsp;&nbsp;&nbsp;'
        #buffer+= '<a href="nr3_after_select">Page 3</a>&nbsp;&nbsp;&nbsp;'
        #buffer+= '<a href="nr4_after_select.html">Page 4</a>&nbsp;&nbsp;&nbsp;'
        #buffer+= '<a href="nr5_after_select.html">Page 5</a>'
    # add date of update
    buffer+= '<h4><i>List updated on '+datetime.datetime.now().strftime("%m/%d/%Y")+'</i></h4>'
    
    for name2,url2,image2,fanart2 in match_file:
        no_image = True
        if debug: print(name2,url2,image2)
        
        if url2 not in ('ignorme','ignoreme'):
            if fanart2 == '<':
                fanart2 = FANART
            else:
                fanart2 = fanart2.replace('<','')
            if Search_filter in name2.lower().replace(' ',''):               
                url2, name2 = render(url2, name2)
                url2 = name2 + '<br>' + url2
                # is image link valid ?
                try:
                    response = requests.get(image2)
                    #print(response)
                    if response.status_code != 200:
                        no_image = True
                        n+=1
                        #replace invalid link image
                        image2='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
                    else:
                        no_image = False
                except:
                    if debug: print(image2,'no image',n,response.status_code)
                    n+=1
                    #print('erreur except')
                    no_image = True
                    #replace invalid image
                    image2='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

                # append list of movies if new
                
                if name2 not in list_movies:
                    new = True
                    list_movies.append(name2)
                    
                    if debug :print(name2,url2,image2)
                    #append buffer if new
                    buffer+='<figure class="swap-on-hover">'
                    buffer+='<img class="swap-on-hover__front-image" src="'+image2+'"/>'
                    buffer+='<div class="swap-on-hover__back-image">'+url2+'</div></figure>'                                        
                    #print each movie results
                    #if True:
                    m+=1
                    print(m,name2,end=' ')
                    if not no_image: 
                        print('*')
                    else:
                        print('#',n)
                # already in list_movies
                else:
                    if not new:
                        print('No new movies for today !')                    
                    break
    # complete with old_list
    buffer += old_list               
    # save list of movies to file

    with open('data/list_movies.txt', 'wb') as fp:
        pickle.dump(list_movies, fp)
        
    #buffer+='<p><small> August 2021</small></p></body></html>'
    return buffer

def find_text(t,sub1,sub2=''):
    start=([m.start() for m in re.finditer(sub1, t)])
    if sub2 != '':
        end=([m.start()+4 for m in re.finditer(sub2, t)])
        return start, end
    return start

def read_match(file):
    # define an empty list
    places = []
    # open file and read the content in a list    
    with open(file, 'r') as filehandle:
        for line in filehandle:
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1].split(',')
            if len(currentPlace)==4:
                # add item to the list
                places.append(currentPlace)
    # print(places[7])
    # for i in range(4):
    #     print(places[7][i])
    return places

def make_dict(places):
    # create dictionary from list
    mydict={}
    
    for name2,url2,image2,fanart2 in places[7:-4]:
        d={}
        name2 = name2.replace('\'','')
        url2 = url2.replace('\'','')
        name2 = name2.replace(')','')
        name2 = name2.replace('(','')
        name2 = name2.replace('[COLOR white]','')
        name2 = name2.replace('[COLORwhite]','')
        name2 = name2.replace('[COLOR gold]','')
        name2 = name2.replace('[COLOR pink]','')
        name2 = name2.replace('[COLORred]','')
        name2 = name2.replace('[B]','')
        name2 = name2.replace('[/COLOR]','\r\n')
        name2 = name2.replace('[/I]','')
        name2 = name2.replace('[I]','')
        name2 = name2.replace('[/B]','')
        url2 = url2.replace("'","")
        image2 = image2.replace("'","").strip()
        fanart2 = fanart2.replace("'","").strip()
        fanart2 = fanart2.replace("<)","")
        if 'sublink' in url2:
            #rectify bad url
            index=url2.find('sublink')
            url2=url2[index:]
            #replace tags
            url2 = url2.replace('sublink:LISTSOURCE:','<a href="')
            url2 = url2.replace('ublink:LISTSOURCE:','<a href="')
            url2 = url2.replace('::LISTNAME:','" target="new">')
            url2 = url2.replace('::#','</a>')
            url2 = url2.replace('\\\\r\\\\n', '<br>')
            url2 = url2.replace('[COLORgold]','')
            url2 = url2.replace('[COLORorchid][/COLOR]','Link to video')
            url2 = url2.replace('[COLORorchid]','')
            url2 = url2.replace('[COLORred]','')
            url2 = url2.replace('[COLORwhite]','')
            url2 = url2.replace('[/COLOR]','')
            
        if debug:print(name2, url2)
        d['url']=url2
        d['img']=image2
        d['fanart']=fanart2
        mydict[name2.strip()]=d
    # end creating dictionary
    return mydict

# saving mydict to file 

def save_json(file, mydict):
    # save as json file
    with open(file, "w") as json_file:
        json.dump(mydict, json_file)
# save_json(file_name)
        


json = 'data/data.json'
def read_json(json):
    with open(json, "r") as json_file:
        mydict = json.load(json_file)
    return mydict
# read_json(json)

def get_key(mydict, k):
    # using loop
    for j,i in enumerate(mydict):
        if (j == k):
            #print ('key',k,i)
            return i        

def last_5():
    print('\n5 last movies from mydict')
    for i,k in enumerate(mydict.keys()):
        if i<5:
            print(i,k,mydict[k]['url'])

def is_image_valid(img):
    try:
        response = requests.get(img)
        if response.status_code == 200:
            return img
    except:
        if debug:
            print(img,'no image',n,response.status_code)
        #replace invalid image
        img='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
    return img

def make_page(mydict, search):
    print('\nMovies from search with : "',search,'"\n')
    n = 0
    titles = []
    for i,k in enumerate(mydict.keys()):    
        if search in k.lower():
            title = k.replace('"','').strip()
            titles.append(title)
            print(n+1,i,title) 
            n+=1
    print('================\n',n,' movies found')
    style ='<html><head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'
    header = style+'<body><h1>Movies with "'+search+'"! </h1>'
    header+= '<h4><i>Rendered on '+datetime.datetime.now().strftime("%m/%d/%Y")+'</i></h4>'
    buffer = ''
    for i,k in enumerate(mydict.keys()):    
        if search in k.lower():
            url2 = '<b>'+k.replace('"','').upper()+'</b><br><br>' + mydict[k]['url']
            #url2 = url2.replace('\\\\r\\\\n','<br>')
            image2 = mydict[k]['img']
            image2 = image2.replace('\'','').strip()
            # is image link valid ?
            image2 = is_image_valid(image2)

            buffer+='<figure class="swap-on-hover">'
            buffer+='<img class="swap-on-hover__front-image" src="'+image2+'"/>'
            buffer+='<div class="swap-on-hover__back-image">'+url2+'</div></figure>'
    f= open("html/search_result.html","w+")
    f.write(header+buffer)
    f.close()
    return titles

def save_pkl(dict1, dict2):
    # save as pickle file
    with open("data/initials.pkl", "wb") as pkl_file:
        pickle.dump(dict1, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
    with open("data/urls.pkl", "wb") as pkl_file:
        pickle.dump(dict2, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
# save_pkl(initials, urls)

def read_pkl(pkl1, pkl2):
    #save dictionaries in pickle files
    with open(pkl1, "rb") as pkl_1:
        mydict1 = pickle.load(pkl_1)
    with open(pkl2, "rb") as pkl_2:
        mydict2 = pickle.load(pkl_2) 
    return mydict1, mydict2
# initials, urls = read_pkl(pkl1, pkl2)


if __name__ == '__main__':  # relatif à libs.py
# pour récupérer les dictionnaires :
# 1: importer de urls
#from urls import initials, urls  
# 2 : lire depuis les fichiers pkl
    initials, urls = read_pkl('../data/initials.pkl', '../data/urls.pkl')
    print(initials.keys())
    print(urls.keys())

else: # relatif au répertoire de makehtmlfile.py
    try:
        from resources.urls import *
    #except:
    #    from urls import *
    except:
        initials, urls = read_pkl(pkl1, pkl2)

# erreur protocol=5 solved (save pckl avec highest_protocol 
# with open("../data/urls2.pkl", "wb") as pkl_file:
#         pickle.dump(initials, pkl_file, protocol=pickle.HIGHEST_PROTOCOL)
# with open("../data/urls2.pkl", "rb") as pkl_1:
#         coucou = pickle.load(pkl_1)
