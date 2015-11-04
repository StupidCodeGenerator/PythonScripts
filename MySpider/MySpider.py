import re
import urllib

def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getUrl(url):
    print(url)
    html = getHtml(url)
    reg = r'[a-zA-z]+://[^\s]*'
    urlReg = re.compile(reg)
    urlList = re.findall(urlReg,html)
    for url in urlList:
        try:
    	   getUrl(url)
        except:
            pass
    return urlList
   
html = getUrl("https://www.jiandan.net")

#for url in result:
#	r = getUrl(url)
#	print(str(len(r)))

#print(html)