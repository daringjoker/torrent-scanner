import urllib3
from bs4 import BeautifulSoup
import os


def getlinks(torrent,site):
#appending the name of torrent and the required site to the search string 
    torrent+="torrent download{}".format(site)
	#replacing the whitespace characters by + 
    torrent=torrent.replace(" ","+")
	#adding the search token to the url
    url="https://www.google.com/search?q={}".format(torrent)
	#send the request to the server and  proceed further only if the server sends correct and complete response
    connection=http.request("get",url)
    if (connection.status==200):
	#parsing the html using the beauthiful soup
        html=connection.data
        soup=BeautifulSoup(html,"html.parser")
		#find all divs where class is r
        linkdivs=soup.find_all(class_="r")
        #print(linkdivs)
        links=[]
        for linkdiv in linkdivs:
		#extracting the link locatio
            linktag=linkdiv.find_all("a")
            for link in linktag:
                linkurl=link["href"]
				#checking for preceding /url?q= tag and removing it to obtain the correct link
                if("/url?q=" in linkurl):
                   linkurl=linkurl.lstrip("/url?q=")
				   #appending all links to a single list
                   links.append(linkurl)
    #returning the list
    return links

def trylinks(links, name):
    for link in links:
        #print("trying "+link)
        torrentpage=http.request("get",link)
        if (torrentpage.status==200 ):
           # print("page obtained")
            html=torrentpage.data
            soup=BeautifulSoup(html,"html.parser")
            for deflink in soup.find_all("a"):
                error=False
                # print(link["href"])
                try:
				#making sure not to let the empty deflink to be parsed
                    title=deflink.contents[0]
                    if (("magnet" in deflink["href"]) | (".torrent" in deflink["href"]) | (name in title) & ("download" in title)):
                        truelink = deflink["href"]
                except:
                    error=True
                finally:
                    if(not error):
                        if (("magnet" in deflink["href"]) | (".torrent" in deflink["href"]) | (name in title) & ("download" in title)):
                            truelink = deflink["href"]
                            if(("http"  not in truelink )& ("magnet" not in truelink)):
                                    linkpieces=link.split("/")
                                    linkhead=linkpieces[0]+"//"+linkpieces[2]
                            else:
                                    linkhead=""
                            complete=linkhead+truelink
                            #print(title)
                            print(complete)



if (__name__ == "__main__") :
	urllib3.disable_warnings()
	http = urllib3.PoolManager()
	sites=[" site:yts.ag"," site:yts.pe"," site:thepiratebay.org"," site:1337x.to"," site:torrentking",""]
	torrent=input("enter name of the torrent you want   ")
	for site in sites:
		links=getlinks(torrent,site)
		trylinks(links,torrent)
	os.system("pause")