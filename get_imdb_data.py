from resources.libs import Open_Url
#import re

# source = 'https://raw.githubusercontent.com/tombebbs1/magicdragon/master/newreleases.txt'
# HTML2 = Open_Url(source)
# #print(HTML2)
# match2 = re.compile('<title>(.+?)</title>.+?<link>(.+?)</link>.+?<thumbnail>(.+?)</thumbnail>.+?<fanart>(.+?)/fanart>',re.DOTALL).findall(str(HTML2))    
# print(match2)

from bs4 import BeautifulSoup


def get_soup(title):
    search= '+'.join(title.split(' ')[:-1])
    source='https://www.imdb.com/search/title/?title='+search #+'&release_date=2021'
    HTML2 = Open_Url(source)
    soup = BeautifulSoup(HTML2, 'html.parser')
    #print(soup.prettify())
    return soup

#soup = get_soup(title)

cl1 = "lister-item mode-advanced"
cl2 = "lister-item-content"

def get_class(soup, cl):
    #myclass = soup.find("div", class_="lister-item mode-advanced")
    myclass = soup.find("div", class_=cl)
    #print(myclass.prettify())
    return myclass

def get_text(cl):
    text = cl.find_all("p", class_="text-muted")[-1]
    return text.contents[0].strip()
    
def get_summary(title):
    soup = get_soup(title)
    myclass1 = get_class(soup, cl1)
    myclass2 = get_class(soup, cl2)

    text = get_text(myclass2)
    #print(text)

    all_p = soup.find_all("p")
    #print(all_p[1:3])
    synopsis = 'Synopsis : '+all_p[1].text.split('...')[0].strip()
    casting = all_p[2].text
    director = ''.join(all_p[2].text.split('\n')[1:3]).strip()
    stars = ''.join(all_p[2].text.split('\n')[4:]).strip()
    summary = '\n'.join([synopsis, director, stars])
    #print(summary)
    return all_p, summary

if __name__ == '__main__':
    title='The Starling (2021)'
    title='This Is the Year (2021)'
    title='Time is up ()'
    title='Chernobyl 1986 (2021)'
    title='East of the Mountains (2021)'
    title = 'There\'s Someone Inside Your House (2021)'
    all_p, summary = get_summary(title)
    print(title)
    print(summary)
    