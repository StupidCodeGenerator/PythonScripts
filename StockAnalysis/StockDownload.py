﻿#http://table.finance.yahoo.com/table.csv?s=000001.sz&d=10&e=27&f=2015&g=d&a=11&b=16&c=1991&ignore=.csv
import urllib2

def DownloadData(url, filename):
	print(url)
	f = urllib2.urlopen(url) 
	with open(filename, "wb") as code:
   		code.write(f.read())

for i in range(1, 999999):
	s = str(i)
	s = s.zfill(6)
	str_url = "http://table.finance.yahoo.com/table.csv?s="+s+".sz&d=10&e=27&f=2015&g=d&a=11&b=16&c=1991&ignore=.csv"
	try:  
	    DownloadData(str_url, s+".csv")
	except:
	    print("null stock")