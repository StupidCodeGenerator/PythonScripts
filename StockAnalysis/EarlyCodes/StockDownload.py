#http://table.finance.yahoo.com/table.csv?s=000001.sz&d=10&e=27&f=2015&g=d&a=11&b=16&c=1991&ignore=.csv
import urllib2
import sys
import os

dataPath = sys.argv[1]

exist = []

for i in os.listdir(dataPath):
    if os.path.isfile(os.path.join(dataPath,i)):
    	exist.append(i)

def DownloadData(url, filename):
	print(url)
	f = urllib2.urlopen(url) 
   	print("SavingFile : " + filename)
	with open(filename, "wb") as code:
   		code.write(f.read())
   	print("Success")

for i in range(1, 999999):
	s = str(i)
	s = s.zfill(6)
	if (s + ".csv") in exist:
		print("exist : " + s + ".csv")
		continue

	print("Try sz")
	str_url = "http://table.finance.yahoo.com/table.csv?s="+s+".sz&d=10&e=27&f=2015&g=d&a=11&b=16&c=1991&ignore=.csv"
	try:  
	    DownloadData(str_url, os.path.join(dataPath, (s + ".csv")))
	except:
	    print("fail")

	print("Try ss")
	str_url = "http://table.finance.yahoo.com/table.csv?s="+s+".ss&d=10&e=27&f=2015&g=d&a=11&b=16&c=1991&ignore=.csv"
	try:
	    DownloadData(str_url, os.path.join(dataPath, (s + ".csv")))
	except:
		print("fail")

