from bs4 import BeautifulSoup

# execute main
# import makehtmlfile

# faire le tri
with open("/home/pi/Documents/Python/streaming/html/nr_vignette.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

#print(soup.prettify(formatter="html"))

mydivs = soup.find_all("figure", {"class": "swap-on-hover"})
header='<head><link rel="stylesheet" type="text/css" href="../resources/style.css"></head>'
txt = ''
refs=[]
last_title=''
debug = False

for div in mydivs:    
    if not ('upstream' in str(div) or 'vidlox' in str(div)) or 'userload.co' in str(div):
        title= div.text.split(')')[0]+')'
        if last_title=='':
            last_title=title
        if debug: print(title)
        txt+=str(div)
        # filter links with valid embbeded iframe
        links = div.find_all("a")
        
        for link in links:
            if not ('upstream' in str(link) or 'vidlox' in str(link) or 'real' in str(link)) or 'userload.co' in str(link):
                if debug: print(link['href'])
                if last_title!=title:
                    refs.append((title, link['href']))
                    last_title=title

import requests
iframes = {}
for title, ref in refs:
    try:
        page = requests.get(ref)
        contents = BeautifulSoup(page.text, 'html.parser')
        here = contents.find_all("div", {"class": "embedbox"})
        try:
            iframe = here[0].textarea.text.strip()
        except:
            pass
        iframe=iframe.replace('width="700"','width=100%').replace('height="430"','height=90%')
        #print(title, iframe)
        iframes[title]=iframe
    except:
        if debug: print('exception',ref)
# with open('/home/pi/Documents/Python/streaming/html/nr_after_select.html','w') as h:
#     h.write(txt.replace('dood.cx','dood.so'))
#     
print('bsoup iframes terminé')
# print(header)
# print(txt)
    