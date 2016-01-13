from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import matplotlib as mpl  
import math
import sys
import os
s = os.sep

def HighLow(data):
	priceData = data[:,6]
	currentPrice = priceData[len(priceData) - 1]
	high = 0
	low = 0
	for p in priceData:
		if p >= currentPrice:
			high += 1
		else:
			low += 1
	if low == 0:
		return 0
	else:
		result = math.log(high / low)
		return result;

def TotalValue(data):
	valueData = data[:,5]
	result = 0
	for v in valueData:
		result += v
	return result

allStockDatas = {}
dataDirectory = sys.argv[1]
for i in os.listdir(dataDirectory):
	fullPath = os.path.join(dataDirectory, i)
	if os.path.isfile(fullPath) and i != "base.csv":
		key = i.split(".")[0]   # get *** from ***.csv
		print("loading file : " + fullPath)
		csvData = sp.genfromtxt(fullPath, delimiter = ",")
		allStockDatas[key] = csvData

result = []
for stockCode in allStockDatas:
	stockData = allStockDatas[stockCode]
	currentPrice = stockData[len(stockData) - 1][6] # the last price
	highLow = HighLow(stockData)
	resultRow = str(highLow) + "," + \
	str(stockCode) + "," + str(TotalValue(stockData))
	print(resultRow)
	result.append(resultRow)

resultPath = os.path.join(sys.argv[2], "HighLow.csv");

with open(resultPath, "a") as file:
	for row in result:
		file.write(row + "\n")
