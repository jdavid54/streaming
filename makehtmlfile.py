# -*- coding: utf-8 -*-
import resources
from resources.libs import getmatch, makebuffer
import time

debug = False
initial = False            # if True search using first letter
Search_filter = ''         # title filter
Search_name = 'doc'        # source name

#pass variable initial to libs
resources.libs.initial=initial
resources.libs.debug=debug
resources.libs.Search_name=Search_name
resources.libs.Search_filter=Search_filter

def main():
    start = time.time()
    match2=getmatch(Search_name)
    print(type(match2))
    buffer=makebuffer(match2)
    end = time.time()
    print('Time of process :',end - start,'s')

    f= open("html\\"+Search_name+"_vignette.html","w+")
    f.write(buffer)
    f.close()
    print("Processus terminé ! "+Search_name+"_vignette.html est créé dans le répertoire html !")

if __name__ == '__main__':
    main()

