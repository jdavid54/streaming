from resources.libs import Open_Url
#import re

# source = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
# HTML2 = Open_Url(source)
# #print(HTML2)
# match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
# print(match2)

import requests
from bs4 import BeautifulSoup

def get_page(url):
    HTML2 = Open_Url(url)
    #HTML2 = requests.get(source, headers=headers)
    soup = BeautifulSoup(HTML2, 'html.parser')
    #print(soup.prettify())
    return soup
    

def get_soup(_title):
    search= '+'.join(_title.split(' ')[:-1])
    source='https://www.imdb.com/search/title/?title='+search #+'&release_date=2021'
    print('Source: ',source)
    #print(search)
    #source = 'https://www.imdb.com/find/?q='+_title
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-User': '?1',}
    
    HTML2 = Open_Url(source)
    #HTML2 = requests.get(source, headers=headers)
    soup = BeautifulSoup(HTML2, 'html.parser')
    #print(soup.prettify())
    return soup

#soup = get_soup(title)

def save(soup):
    file = open('soup.html', 'bw')
    s=soup.encode('utf8')
    file.write(s)
    file.close()

def get_class(soup, cl):  # first item with class= cl
    #myclass = soup.find("div", class_="lister-item mode-advanced")
    #myclass = soup.find("div", class_=cl)
    myclass = soup.find("a", class_=cl)
    #print(myclass.prettify())
    return myclass

def get_href(soup, cl):  # first item with class= cl
    #myclass = soup.find("div", class_="lister-item mode-advanced")
    #myclass = soup.find("div", class_=cl)
    try:
        href = soup.find("a", class_=cl)['href']
        #print(myclass.prettify())
        return href
    except:
        return None
    

def get_text(soup):
    section = soup.find("section", class_='sc-69e49b85-4 ktjuZl')
    #synop = soup.find("span", class_='sc-466bb6c-2')
    children=[]
    for t in section.children:
        children.append(t)
        #teams.append(t.a.contents[0].strip())
    synop = children[1].span.contents[0].strip()
    real = children[2].a.contents[0].strip()
    act = [c for c in children[2].children]  #.a.contents[0].strip()
    return synop, real, act
    
def get_summary(_title,cl='ipc-title-link-wrapper'):
    soup = get_soup(_title)
    #myclass1 = get_class(soup, cl1)
    #myclass2 = get_class(soup, cl2)
    myhref = soup.find("a", class_=cl)['href']
    if myhref == None:
        return f"No href found for {title}"
    #print(myhref)
    url='https://www.imdb.com'+myhref
    print('href: ',url)
    
    soup = get_page(url)
    
    # get data
    #print(soup)

    summary = []
    synop_cl = "sc-466bb6c-1 dWufeH"
    synop = soup.find("span",class_=synop_cl)
    #print("Synop: "+synop.contents[0].strip())
    summary.append("Synopsis: "+synop.contents[0].strip())

    div_cl = "sc-410d722f-1 lgrCIy"
    div1 = soup.find_all("div",class_=div_cl)
    #print(div1, len(div1))

    container = "ipc-metadata-list-item__content-container"
    div2 = div1[0].find_all("div",class_=container)
    #print(div2, len(div2))

    a_cl = "ipc-metadata-list-item__list-content-item"
    titles = ["Director: ","Writers: ","Stars: "]

    for k in range(len(div2)):
        value = ""
        #print(titles[k],end=": ")
        value += titles[k] 
        a_data = div2[k].find_all("a",class_=a_cl)
        for m in range(len(a_data)):
            value += a_data[m].contents[0].strip()+","
            #print(a_data[m].contents[0].strip(),end=', ') #, len(a_data))
        #print()
        summary.append(value[:-1])
    summary = '\n'.join(summary)
            
    '''  
    #   synopsis = 'Synopsis : '+ synop.contents[0].strip()
    #   director = 'Director : '+ 
    #   writers = 'Writers : '+
    #   stars = 'Stars : '+
    #   casting = all_p[2].text
    #   director = ''.join(all_p[2].text.split('\n')[1:3]).strip()
    #     stars = ''.join(all_p[2].text.split('\n')[4:]).strip()
    #summary = '\n'.join([synopsis, director, writers, stars])
    
    #spans = text[0].find_all("span")
    #certif = text[0].find(class_='certificate').text
    try:
        runtime = text[0].find(class_='runtime').text
        ghost = text[0].find(class_='ghost').text
        genre = text[0].find(class_='genre').text
    except:
        runtime=''
        ghost=''
        genre=''
    data = ''
    data += ''.join(['\nRuntime=',runtime])
    data += ''.join(['\nGhost=',ghost])
    data += ''.join(['\nGenre=',genre.strip()])
    #print(summary)
    return all_p, ''.join([summary, data])
    '''
    return summary

if __name__ == '__main__':    
    title = 'SPAGHETTI (2023)'
    #cl = 'ipc-title-link-wrapper'
    '''
    soup = get_soup(title)
    myhref = get_href(soup, cl) 
    #print(cl,myhref)
    url='https://www.imdb.com'+myhref
    print('url:',url)
    soup = get_page(url)
    '''
    summary = get_summary(title)
    #_all_p, summary_data = get_summary(title)
    #print(title)
    print(summary)
    