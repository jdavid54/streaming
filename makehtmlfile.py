#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import resources
from resources.libs import getmatch, makebuffer
import time

import requests
import re

# last total = 622
# doublon = 3

def main():
    debug = False
    initial = False        # if True search using first letter
    do_all = False         # if True make html page from scratch else complete with old one data
    limit = 'Spiderhead (2022)'
    
    Search_filter = ''     # title filter
    Search_name = 'nr'     # change here nr, nr2, nr3, n4, n5 .... ! for initial search, use argument -i
    text_file = 'data/match.txt'
    
    start = time.time()
    
    # from line command
    args = sys.argv
    if '-d' in args:
        debug = True
    if '-i' in args:
        initial = True
    if '-n' in args:
        Search_name = args[args.index('-n')+1]
    
    #pass variable initial to libs
    resources.libs.initial = initial
    resources.libs.debug = debug
    resources.libs.Search_name = Search_name
    resources.libs.Search_filter = Search_filter
    resources.libs.data_file = text_file
    resources.libs.do_all = do_all
    resources.libs.limit = limit
    #match2 = getmatch(Search_name)  # get the file from 'nr', or,'nr2', ...
    #print(match2)
    

    url = 'https://raw.githubusercontent.com/tombebbs1/MagicDragonKodi18/main/newreleases1.xml'
    response = requests.get(url)
    #print(response.content)
    HTML2 = response.content.decode("utf8")
    match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
    text_file = 'data/match.txt'
    #print(match2[2:4])
    
    buffer, new = makebuffer(match2)
    #print(buffer)
    end = time.time()
    print('Time of process :',end - start,'s')
    
    # create index.html
    with open("html/index.html","wb+") as f:
        f.write(buffer)
        print("Processus terminé ! index.html est créé dans le répertoire html !")
        #f.close()
    
    # create nr_vignette.html
    with open("html/"+Search_name+"_vignette.html","wb+") as f:
        f.write(buffer)
        print("Processus terminé ! " + Search_name + "_vignette.html est créé dans le répertoire html !")
        #f.close()
    
    
    
    # save to local web server
    #if Search_name == 'nr':      
    #    with open("/var/www/html/streaming/html/nr_vignette.html","w") as f:
    #        f.write(buffer)        
          
    return new

if __name__ == '__main__':
    new = main()
    #import synopsis
    # ftp - edit credentials before
    if new:
        import ftp_streaming
        import synopsis
    
