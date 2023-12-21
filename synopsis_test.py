from get_imdb_data import *

def local_get_summary(title):
    cl = 'ipc-title-link-wrapper'
    soup = get_soup(title)
    myhref = get_href(soup, cl) #soup.find("a", class_=cl)['href']
    if myhref == None:
        return f"No href found for {title}"
    #print(cl,myhref)
    url='https://www.imdb.com'+myhref
    print('url:',url)
    soup = get_page(url)
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
    #print(summary)
    return summary

# MAJ titre dans dict
import synopsis
mydict=synopsis.load_json()

title = 'Girls from Dubai (2021)'  # error no synopsis
#title = 'Maestro (2023)'
try:
    mydict[title]= local_get_summary(title)
    #mydict[title]= get_summary(title)   # from get_imdb_data.py
    print(mydict[title])
except:
    print(f"No synopsis found for {title}")


#synopsis.save_dict(mydict)
