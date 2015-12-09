from __future__ import division
import numpy as np
import scipy as sp
import urllib2
import sys
import os

BASE_INDEX = {"LAST_DATE":0 , "CURRENT_PRICE":1}
STOCK_DATA_INDEX = {"CODE":0, "OPEN":1, "HIGH":2, "LOW":3 "CLOSE":4 \
					"VOLUME":5, "ADJ_CLOSE":6}

# Load from directory/base.csv and store by rows.
# Each row stores one stock info
# Need to be loaded at the begining of the program starts.
# The key is the stock code
# The value will be a array of CurrentPrice and LastDate
stockBase = {}

# Load content in directory/base.csv and store into stockBase
def LoadStockBase(directory):
	print("LoadingBase...")
	filePath = os.path.join(directory, "base.csv")
	baseString = ""
	with open(filePath, "r") as file:
		baseString = file.read()
		print(baseString)
	if baseString:
		stockBaseArray = sp.genfromtxt(filePath, delimiter=",")
		for stockData in stockBaseArray:
			key = stockData[0]
			stockBase[key] = stockBaseArray[1:]

# It will update the stock info of the given key in stockBase.
def UpdateStockBase(stockCode, lastDate, currentPrice):

# Download from url and return the result as a file pointer
def DownloadStock(startDate, endDate, code, directory):
	start_ymd = startDate.split("-")
	end_ymd = endDate.split("-")
	# the month should -1 because the yahoo api is like that ...
	start_ymd[1] = str(int(start_ymd[1]) - 1)
	end_ymd[1] = str(int(end_ymd[1]) - 1)
	result = ""
	print("Try sz")
	try:
		str_url = "http://table.finance.yahoo.com/table.csv?s="+code+\
			".sz&d="+end_ymd[1]+"&e="+end_ymd[2]+"&f="+end_ymd[0]+\
			"&g=d&a="+start_ymd[1]+"&b="+start_ymd[2]+"&c="+start_ymd[0]+\
			"&ignore=.csv"
		print("Downloading : " + str_url)
		result = urllib2.urlopen(str_url).read()
	except:
		print("Try ss")
		str_url = "http://table.finance.yahoo.com/table.csv?s="+code+\
			".ss&d="+end_ymd[1]+"&e="+end_ymd[2]+"&f="+end_ymd[0]+\
			"&g=d&a="+start_ymd[1]+"&b="+start_ymd[2]+"&c="+start_ymd[0]+\
			"&ignore=.csv"
		print("Downloading : " + str_url)
		result = urllib2.urlopen(str_url).read()
	if result:
		# I don't know why [1:-1:-1] dosen't work
		rows = result.split("\n")[1:-1]
		rows = rows[::-1]
		print(rows)
		with open(str(code) + ".csv", "a") as file:
			for row in rows:
				file.write(row + "\n");
		print("File write to : " + str(file))
		currentPrice = rows[len(rows) - 1][6]

# ---------------------------------------------------
# START

DownloadStock("2015-10-01", "2015-10-30", "000001", "./")
