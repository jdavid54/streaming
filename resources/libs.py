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
#import datetime
#import shutil
import re
#import os
try:
    import json
except:
    import simplejson as json
#import time
import requests
#import _Edit

style='<html><head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'

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
        elif Search_title[0] in '':
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
    source=chooseURL(Search_name)
    if debug: print(Search_name,source,Search_filter)
    print(Search_name,source)
    HTML2 = Open_Url(source)
    match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))
    if debug:
        f= open("match2.txt","w+")
        f.write(str(match2))
        f.close()
    return match2

def linkok(link):
    test=True
    for sub in ('vidto','vidzi'):
        if link.find(sub) != -1:
            test=False
    return test

def makebuffer(match_file):
    FANART = 'fanart.jpg'
    n=1                     # error image
    m=1                     # number of movies
    buffer=style+'<body><h1>'+Search_name+' movies ! Enjoy !</h1>'
    for name2,url2,image2,fanart2 in match_file:
        if debug: print(name2,url2,image2)
        if url2 not in ('ignorme','ignoreme'):
            if fanart2 == '<':
                fanart2 = FANART
            else:
                fanart2 = fanart2.replace('<','')
            if Search_filter in name2.lower().replace(' ',''):
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
                url2=name2+'<br>'+url2
                # is image link valid ?
                try:
                    response = requests.get(image2)
                    if response.status_code != 200:
                        n+=1
                        #replace invalid link image
                        image2='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'

                except:
                    if debug: print(image2,'no image',n,response.status_code)
                    n+=1
                    #replace invalid image
                    image2='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'


                if debug :print(name2,url2,image2)
                #append buffer
                buffer+='<figure class="swap-on-hover">'
                buffer+='<img class="swap-on-hover__front-image" src="'+image2+'"/>'
                buffer+='<div class="swap-on-hover__back-image">'+url2+'</div></figure>'
                print(m,name2,end=' ')
                if linkok(url2): 
                    print('*')
                else:
                    print()
                m+=1
    buffer+='<p><small> May 2019</small></p></body></html>'
    return buffer
