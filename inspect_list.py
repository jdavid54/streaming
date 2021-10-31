# read from match.txt, process the text to produce a dictionary dict
# and save it in a json data file (data.json) and a pickle data file (data.pkl) in directory data
# make a html page (search_page.html) with a selection of data from dict fitting a search word and save it in html directory


import datetime
import requests

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
    dict={}
    
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
        dict[name2.strip()]=d
    # end creating dictionary
    return dict

# saving dict to file 
import json
import pickle

def save2file(dict):
    # save as json file
    a_file = open("data/data.json", "w")
    json.dump(dict, a_file)
    a_file.close()
    # save as pickle file
    a_file = open("data/data.pkl", "wb")
    pickle.dump(dict, a_file)
    a_file.close()


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

def get_key(dict, k):
    # using loop
    for j,i in enumerate(dict):
        if (j == k):
            #print ('key',k,i)
            return i        

def last_5():
    print('\n5 last movies from dict')
    for i,k in enumerate(dict.keys()):
        if i<5:
            print(i,k,dict[k]['url'])


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


def search(d, what):
    print('\nMovies from search with : "',what,'"\n')
    n = 0
    for i,k in enumerate(d.keys()):    
        if what in k.lower():
            print(n+1,i,k.replace('"','').strip()) 
            n+=1
    print('================\n',n,' movies found')

def make_page(d, what):
    search(d, what)
    style='<html><head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'
    buffer=style+'<body><h1>Movies with "'+what+'"! </h1>'
    buffer+= '<h4><i>Rendered on '+datetime.datetime.now().strftime("%m/%d/%Y")+'</i></h4>'

    for i,k in enumerate(d.keys()):    
        if what in k.lower():
            url2 = '<b>'+k.replace('"','').upper()+'</b><br><br>'+d[k]['url']
            #url2 = url2.replace('\\\\r\\\\n','<br>')
            image2 = d[k]['img']
            image2 = image2.replace('\'','').strip()
            # is image link valid ?
            image2 = is_image_valid(image2)

            buffer+='<figure class="swap-on-hover">'
            buffer+='<img class="swap-on-hover__front-image" src="'+image2+'"/>'
            buffer+='<div class="swap-on-hover__back-image">'+url2+'</div></figure>'
    f= open("html/search_result.html","w+")
    f.write(buffer)
    f.close()

def main(file, save=False):
    places = read_match(file)
    mydict = make_dict(places)
    if save:
        save2file(mydict)
    #search = '2021'
    #search = 'night'
    #search = 'love'
    #search = 'jungle'
    #search ='house'
    what = 'sangre'
    make_page(mydict, what)

    print('Nombre de films :',len(mydict))
    print('Last movie name\n',get_key(mydict,0))
    print('Last movie data\n',mydict[get_key(mydict,0)])

debug = False
save = False

if __name__ == '__main__':
    file = '/home/pi/Documents/Python/streaming/data/match.txt'
    main(file)