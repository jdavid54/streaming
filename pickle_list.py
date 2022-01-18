import pickle

# réduire les titres mal renseignés pour reconstruire la page à partir '

with open ('data/list_movies.txt', 'rb') as fp:
    list_movies = pickle.load(fp)
                
#print(list_movies[-53:])
l = len(list_movies)
print(l) 
print(list_movies)
#new_list = list_movies[:l-53]
#print(new_list)


'''
with open('data/list_movies.txt', 'wb') as fp:
        pickle.dump(new_list, fp)
'''
import re
import requests
url = 'https://raw.githubusercontent.com/tombebbs1/MagicDragonKodi18/main/newreleases1.xml'
response = requests.get(url)
#print(response.content)
HTML2 = response.content.decode("utf8")
match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    

mov = ['Red Stone (2021)','Try Harder! (2021)','Echoes of the Past (2021)', 'The Runner (2022)',
"This Game's Called Murder (2021)", 'The Spine of Night (2021)', 'The Perfect Pairing (2022)', 'Cyrano (2021) Screener', "The King's Daugter (2022)"]

for k in range(len(list_movies)):
    if list_movies[k] in mov:
        print(k, list_movies[k])
        
for m in mov:
    if m in list_movies:
        print(m)
    
    