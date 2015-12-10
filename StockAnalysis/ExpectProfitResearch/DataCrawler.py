# -- Data Structure --
# base: code(key), lastDate, currentPrice
# stock: code(key), open, high, low, close, volume, adjClose

from __future__ import division
import numpy as np
import scipy as sp
import urllib2
import sys
import os
import datetime

# Load content in directory/base.csv
def LoadStockBase(directory):
	stockBase = {}
	print("LoadingBase...")
	filePath = os.path.join(directory, "base.csv")
	baseString = ""
	try:
		with open(filePath, "r") as file:
			baseString = file.read()
			print(baseString)
	except:
		os.mkdir(directory)
		with open(filePath, "a") as file:
			file.write("")
			print("Create new base file")
	if baseString:
		baseLines = baseString.split("\n")
		for line in baseLines:
			colums = line.split(",")
			key = colums[0]
			stockBase[key] = colums[1:]
	return stockBase

# It will update the stock info of the given key in stockBase.
def UpdateStockBase(stockCode, lastDate, currentPrice, stockBase, directory):
	stockArray = [lastDate, currentPrice]
	stockBase[stockCode] = stockArray
	filePath = os.path.join(directory, "base.csv")
	print("Updating base : " + filePath)
	print(stockBase)
	with open(filePath, "wb") as file:
		for key in stockBase:
			string = str(key) +","+ str(lastDate) +","+ str(currentPrice) + "\n"
			file.write(string)

# Download from url and return the result as a file pointer
def DownloadStock(startDate, endDate, code, directory, stockBase):
	start_ymd = startDate.split("-")
	end_ymd = endDate.split("-")
	# the month should -1 because the yahoo api is like that ...
	start_ymd[1] = str(int(start_ymd[1]) - 1).zfill(2)
	end_ymd[1] = str(int(end_ymd[1]) - 1).zfill(2)
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
		print("Fail...")
	if not result:
		try:
			print("Try ss")
			str_url = "http://table.finance.yahoo.com/table.csv?s="+code+\
				".ss&d="+end_ymd[1]+"&e="+end_ymd[2]+"&f="+end_ymd[0]+\
				"&g=d&a="+start_ymd[1]+"&b="+start_ymd[2]+"&c="+start_ymd[0]+\
				"&ignore=.csv"
			print("Downloading : " + str_url)
			result = urllib2.urlopen(str_url).read()
		except:
			print("Fail...")
	if result:
		# I don't know why [1:-1:-1] dosen't work
		rows = result.split("\n")[1:-1]
		rows = rows[::-1]
		filePath = os.path.join(directory, str(code) + ".csv")
		with open(filePath, "a") as file:
			for row in rows:
				file.write(row + "\n");
		print("File write to : " + str(filePath))
		lastRowData = rows[len(rows) - 1].split(",")
		currentPrice = lastRowData[6]
		lastDate = lastRowData[0]
		print("LastRow : " + rows[len(rows) - 1])
		UpdateStockBase(code, lastDate, currentPrice, stockBase, directory)

# ---------------------------------------------------
# START

# 1. Load the stock base and calculate today
stockBase = LoadStockBase(sys.argv[1])
today = str(datetime.date.today())
print("Today : " + today)

# 2. Try to download all stocks. before that, check if it exists in base
#    If so, download missing dates
for i in range(1, 999999):
	stockCode = str(i).zfill(6)
	if stockBase.has_key(stockCode):
		lastDate = stockBase[stockCode][0]
		print("lastDate" + lastDate)
		DownloadStock(lastDate, today, stockCode, sys.argv[1], stockBase)
	else:
		print("New Stock : " + stockCode)
		DownloadStock("1991-11-16", today, stockCode, sys.argv[1], stockBase)