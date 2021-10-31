# same as inspect_list.py
# read from match.txt to create a json file from mydict
# save to file if save = True
# make a html file if make = True

import datetime
import requests

debug = False
save = True
make = False
test = False

code = 'nr'

if code=='nr':
    file = '/home/pi/Documents/Python/streaming/data/match.txt'
    data_json = "data/data2.json"
    data_pkl = "data/data2.pkl"

if code=='nr2':
    file = '/home/pi/Documents/Python/streaming/data/match2.txt'
    data_json = "data/data3.json"
    data_pkl = "data/data3.pkl"

if test:
    file = '/home/pi/Documents/Python/streaming/data/match_test.txt'
    data_json = "data/data_test.json"
    
'''
datetime_object = datetime.datetime.now()
print(datetime_object)

print(datetime_object.strftime("%d/%m/%Y, %H:%M:%S"))
'''

def find_text(t,sub1,sub2=''):

    start=([m.start() for m in re.finditer(sub1, t)])
    if sub2 != '':
        end=([m.start()+4 for m in re.finditer(sub2, t)])
        return start, end
    return start

# f= open("/home/pi/Documents/Python/streaming/match.txt","r")
# match_file = f.read()
# f.close()

# define an empty list
places = []
# open file and read the content in a list
with open(file, 'r') as filehandle:
    for line in filehandle:
        if 'ignor' not in line:
            #print(line)
            # remove linebreak which is the last character of the string
            currentPlace = line[:-1].split(',')
            #print(currentPlace)
            if len(currentPlace)==4:
                # add item to the list
                places.append(currentPlace)

# print(places[7])
# for i in range(4):
#     print(places[7][i])

# create dictionary from list
mydict={}
mydict['movies']=['']*len(places)
#k=0
#for name2,url2,image2,fanart2 in places:
for k,(name2,url2,image2,fanart2) in enumerate(places):
    if test: print(k,name2)
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
    if test: print(name2)
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
    d['name']=name2.strip()
    if test: print(d)
    mydict['movies'][k]=d
    #k+=1

# end creating dictionary
print(len(mydict['movies']))


# saving dict to file 
import json
import pickle

def save2file(mydict):
    # save as json file
    a_file = open(data_json, "w")
    json.dump(mydict, a_file)
    a_file.close()
    # save as pickle file
    a_file = open("data_pkl", "wb")
    pickle.dump(mydict, a_file)
    a_file.close()

if save:
    save2file(mydict)


# access to dictionary element
# print(mydict['movies'][100]['name'])
# print(mydict['movies'][100]['img'])
# print(mydict['movies'][100]['url'])

'''
# reading from file
file_name= 'data/data.pkl'
def read_pkl(file_name):
    a_file = open(file_name, "rb")
    output = pickle.load(a_file)
    print(output)

file_name= 'data/data.json'
def read_json(file_name):
    a_file = open(file_name, "r")
    output = a_file.read()
    print(output)
'''

def get_key(mydict, k):  # for mydict structure : { movie_name1 : {url1, img1, fanart1}, movie_name2 : {url2, img2, fanart2} ...}
    # using loop
    for j,i in enumerate(mydict):
        if (j == k):
            print ('key',k,i)
            return i        
# print('Last movie\n', mydict[get_key(mydict,0)])

# mydict structure : { 'movies' : {name1, url1, img1, fanart1}, {name2, url2, img3, fanart3} ...}
print('Last movie\n', mydict['movies'][0])


def last_5():
    print('\n5 last movies from mydict')
    for i,k in enumerate(mydict.keys()):
        if i<5:
            print(i,k,mydict[k]['url'])


def is_image_valid(img):
    try:
        response = requests.get(img)
        if response.status_code != 200:
            n+=1
            #replace invalid link image
            img='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
    except:
        if debug: print(img,'no image',n,response.status_code)
        n+=1
        #replace invalid image
        img='https://upload.wikimedia.org/wikipedia/commons/a/ac/No_image_available.svg'
    return img

def make_page(search):
    print('\nMovies from search with : "',search,'"\n')
    n = 0
    for i,k in enumerate(mydict.keys()):    
        if search in k.lower():
            print(n+1,i,k.replace('"','').strip()) #, mydict[k]['url'])
            n+=1
    print('================\n',n,' movies found')
    style='<html><head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'
    buffer=style+'<body><h1>Movies with "'+search+'"! </h1>'
    buffer+= '<h4><i>Rendered on '+datetime.datetime.now().strftime("%m/%d/%Y")+'</i></h4>'

    for i,k in enumerate(mydict.keys()):    
        if search in k.lower():
            url2 = '<b>'+k.replace('"','').upper()+'</b><br><br>'+mydict[k]['url']
            #url2 = url2.replace('\\\\r\\\\n','<br>')
            image2 = mydict[k]['img']
            image2 = image2.replace('\'','').strip()
            # is image link valid ?
            image2 = is_image_valid(image2)

            buffer+='<figure class="swap-on-hover">'
            buffer+='<img class="swap-on-hover__front-image" src="'+image2+'"/>'
            buffer+='<div class="swap-on-hover__back-image">'+url2+'</div></figure>'
    f= open("html/search_result.html","w+")
    f.write(buffer)
    f.close()

#search='2021'
search='night'
#search='love'
#search = 'jungle'
search='house'
search='black'

if make:
    make_page(search)
