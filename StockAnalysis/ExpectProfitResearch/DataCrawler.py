#
# 1. Use MongodDB as database. Using database is always good. 
#    If I don't use these days, I will use that later. 
#    So I just use that by learning
# 2. Download from yahoo finace.
# 3. DataStructure is
#    { Date(key), Open, High, Low, Close, Valume, AdjClose }.
#    And the database name is StockData.StockName
#

from __future__ import division
import numpy as np
import scipy as sp
import urllib2
from pymongo import MongoClient
from io import StringIO

# Download from url and return the result as a file pointer
def DownloadUrl(url):
	result = ""
	print("Downloading : " + url)
	f = urllib2.urlopen(url) 
	return f

# It will translate 2015/1/1 into 20150101 as a number
# because it's clearer
def DateTranslate(timeString):
	try:
		yearMonthDay = timeString.split("/")
		year = int(yearMonthDay[0])
		month = int(yearMonthDay[1])
		day = int(yearMonthDay[2])
		return year * 10000 + month * 100 + day
	except:
		return -1

# The string is actually a csv. This function will split that csv
# Then save each line into mongodb
def SaveDataToMongo(filePointerOfUrl, collectionName):
	client = MongoClient()
	db = client.StockData
	collection = db[collectionName]
	csvData = sp.genfromtxt(filePointerOfUrl, delimiter=",")
	posts = []
	for row in csvData:
		if(sp.isnan(row[1])):  # the open price is always number
			continue
		post = {}
		post["date"] = DateTranslate(row[0])
		post["open"] = row[1]
		post["high"] = row[2]
		post["low"] = row[3]
		post["close"] = row[4]
		post["valume"] = row[5]
		post["adjClose"] = row[6]
		posts.append(post)
	collection.insert_many(posts)

# START
# ---------------------------------------------------

str_url = "http://table.finance.yahoo.com/table.csv?s="+"000001"+\
		".sz&d=10&e=27&f=2015&g=d&a=10&b=20&c=2015&ignore=.csv"
result = DownloadUrl(str_url)
SaveDataToMongo(result, "s000001")