#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  6 09:42:45 2019

@author: jeandavid
"""
import re
import sys
import resources
from resources.libs import getmatch, makebuffer
import time
from urllib.request import urlopen, Request

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

debug = False
initial = False 
resources.libs.initial=initial
resources.libs.debug=debug

HTML2 = Open_Url('http://supremacy.org.uk/tombraider/dogsbollocks/newreleases.txt')
print(HTML2)
'''
prog = re.compile(pattern)
result = prog.match(string)
   is equivalent to
result = re.match(pattern, string)
'''

pattern=re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL)
#pattern=re.compile('<title>(.+?)</title>',re.DOTALL)  #au moins un acaractere entre les tags title
#pattern=re.compile('<link>(.+?)</link>',re.DOTALL)
#pattern=re.compile('<link>(.+?)</link>')
#print(type(pattern))
match2 = pattern.findall(str(HTML2))
print('+++++++++++++++++++++++++++++++++++++++\n',match2[7])
#match=getmatch('nr')
#print (match2[7])
#print('=====')
#print(match2[9])
tags=['title','link','thumbnail','fanart']
for i in (7,8,9):
    number=0
    for k in match2[i]:
        print(tags[number])
        print(i,k,'\n')
        number+=1

print('>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>')
#extract url from each item with multi sublinks 
print(match2[7][1])
#using re.compile
p=re.compile('sublink:LISTSOURCE:(.+?)::LISTNAME')  #(.+?) = all between sub.. and ::LISTN..
for k in match2[7]:
    #print(k)
    sublink=p.findall((k))
    if sublink != []:print('-------------------------\n',sublink)
print('<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<')    
#print([k for k in match2[7]])

# using split
for k in match2[7]:
    if 'sublink' in k:
        subs=k.split('sublink:LISTSOURCE:') 

    for k in subs:
        #print(k) 
        #print('------------------------------------') 
        links=k.split('::LISTNAME')  
        if 'http' in links[0]:
            print(links[0])

