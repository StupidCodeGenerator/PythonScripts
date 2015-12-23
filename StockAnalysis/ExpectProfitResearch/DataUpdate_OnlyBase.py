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
import traceback

MARKET_WORD = {"600":"ss", "601":"ss", "900":"ss", "730":"ss", \
				"700":"ss", "603":"ss",\
				"080":"sz", "000":"sz", "002":"sz", "300":"sz"}

def GetAllStockCodes():
	result = []
	prefixs = ["600", "601", "603", "900", "730", "700", "080", \
				"000", "002", "300"]
	for prefix in prefixs:
		for i in range(0,1000):
			postFix = str(i).zfill(3)
			result.append(prefix + postFix)
	return result;

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
		with open(filePath, "a") as file:
			file.write("")
			print("Create new base file")
	if baseString:
		baseLines = baseString.split("\n")
		for line in baseLines:
			if(line != ""):
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
	with open(filePath, "wb") as file:
		for key in stockBase:
			string = str(key) +","+ str(stockBase[key][0]) +","+ \
									str(stockBase[key][1]) + "\n"
			file.write(string)

def DownloadStock(startDate, endDate, code, directory, stockBase):
	start_ymd = startDate.split("-")
	end_ymd = endDate.split("-")
	# the month should -1 because the yahoo api is like that ...
	start_ymd[1] = str(int(start_ymd[1]) - 1).zfill(2)
	end_ymd[1] = str(int(end_ymd[1]) - 1).zfill(2)
	# if last day is just today, interrupt
	if(start_ymd[0] == end_ymd[0] and start_ymd[1] == end_ymd[1] and \
								int(end_ymd[2]) - int(start_ymd[2]) <= 1):
		print(code + " is up-to-date")
		return;
	result = ""
	marketWorkd = MARKET_WORD[code[0:3]]
	try:
		str_url = "http://table.finance.yahoo.com/table.csv?s="+code+\
			"."+marketWorkd+"&d="+end_ymd[1]+"&e="+end_ymd[2]+"&f="+end_ymd[0]+\
			"&g=d&a="+start_ymd[1]+"&b="+start_ymd[2]+"&c="+start_ymd[0]+\
			"&ignore=.csv"
		print("Downloading : " + str_url)
		result = urllib2.urlopen(str_url).read()
	except:
		print(traceback.format_exc())
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

stockBase = LoadStockBase(sys.argv[1])
today = str(datetime.date.today())
print("Today : " + today)

count = []
count.append(0)

for stockCode in stockBase.keys():
	count[0] += 1
	print("["+str(count[0])+"/"+str(len(stockBase))+"]")
	lastDate = stockBase[stockCode][0]
	print("LastDate : " + lastDate)
	DownloadStock(lastDate, today, stockCode, sys.argv[1], stockBase)