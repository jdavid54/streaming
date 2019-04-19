# -*- coding: utf-8 -*-
import resources
from resources.libs import *

debug = False
initial = False            # if True search using first letter
Search_filter = ''         # title filter
Search_name = 'action'     # source name

#pass variable initial to libs
resources.libs.initial=initial
resources.libs.debug=debug
resources.libs.Search_name=Search_name
resources.libs.Search_filter=Search_filter

def main():
    match2=getmatch(Search_name)
    buffer=makebuffer(match2)

    f= open('html/'+Search_name+"_page.html","w+")
    f.write(buffer)
    f.close()
    print("Processus terminé ! "+Search_name+"_page.html est créé dans le répertoire html !")

if __name__ == '__main__':
    main()

