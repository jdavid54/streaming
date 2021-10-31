# -*- coding: utf-8 -*-
import sys
import resources
from resources.libs import getmatch, makebuffer
import time

def main():
    debug = False
    initial = False        # if True search using first letter
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
    #else:
    #    Search_name = 'nr'
    
    #pass variable initial to libs
    resources.libs.initial = initial
    resources.libs.debug = debug
    resources.libs.Search_name = Search_name
    resources.libs.Search_filter = Search_filter
    resources.libs.data_file = text_file
    
    match2 = getmatch(Search_name)  # get the file from 'nr', or,'nr2', ...
    #print(type(match2))
    buffer = makebuffer(match2)
    end = time.time()
    print('Time of process :',end - start,'s')

    f= open("html/"+Search_name+"_vignette.html","w+")
    f.write(buffer)
    f.close()
    print("Processus terminé ! "+Search_name+"_vignette.html est créé dans le répertoire html !")

'''
if __name__ == '__main__':
    main()
'''
main()

