# The relationship between (currentPrice/fitPrice) and Avr(MaxPrice in Next N Days)
# and Avr(MinPrice in Next N Days)

from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import math
import sys
import os
s = os.sep

def ReadDatas(dataDirectory):
	datas = []
	for fileName in os.listdir(dataDirectory):
		fullPath = os.path.join(dataDirectory, fileName);
		print("LOADING : " + fullPath)
		if os.path.isfile(fullPath):
			datas.append(sp.genfromtxt(fullPath, delimiter=","))
	return datas[::-1] # because the original data is from late to early

# It will try to fit the price in lognorm.
# then return the price that has max probability
def FitPrice(data):
	priceData = data[:,4]
	priceData = priceData[~sp.isnan(priceData)]
	shape, loc, scale = lognorm.fit(priceData,loc = 0)
	x = np.linspace(0, 100, 100)
	p = lognorm.pdf(x, shape, loc, scale)
	maxIndex = 0
	for i in range(0, len(p)):
		if p[i] >= p[maxIndex]:
			maxIndex = i
		else:
			break; # if the plot goes down, stop searching.
	return x[maxIndex]

# Return actual price, has noting to do with FitPrice and CurrentPrice
def PriceAfterNDays(data, currentDay, n):
	return data[currentDay + n - 1][4]  # Give the last day's price

# This function will write the result to dicts above
# These two parameters below will save the result
# The "profitResult" is a dict, key is buy-in price, value is profit after n days.
# The "dataQuantities" is a dict, key is by-in price, value is the quantity of that key in data.
# So you can use profitResult[key]/dataQuantities[key] to get the expection of profit.
def ProfitStatInNDays(data, n, profitResult, dataQuantities):
	fitPrice = FitPrice(data)
	if fitPrice == 0:
		return
	for i in range(0, len(data) - n):
		if not (sp.isnan(data[i][1]) or sp.isnan(data[i][4]) or sp.isnan(data[i][5])):
			if data[i][5] > 0: # Avoid the days that stops dealing
				maxPossiblePriceAfterNDays = PriceAfterNDays(data, i, n) / fitPrice
				currentPrice = data[i][4] / fitPrice  
				key = (currentPrice // 0.05) * 0.05                 # granulate current price
				value = maxPossiblePriceAfterNDays - currentPrice   # expect growth
				if profitResult.has_key(key):
					profitResult[key] += value
					dataQuantities[key] += 1
				else:
					profitResult[key] = value
					dataQuantities[key] = 1


# It will return a dict, the key is buy-in price, the value is the expected profit
def ProfitCurve(n, datas):
	dataQuantities = {}
	profitResult = {}
	for data in datas:
		ProfitStatInNDays(data, n, profitResult, dataQuantities)
	output = {}
	for key in profitResult:
		output[key] = profitResult[key] / dataQuantities[key]
	return output


# START
########################################################################
dataDirectory = sys.argv[1]
resultDirectory = sys.argv[2]

exist = []
for i in os.listdir(resultDirectory):
	if os.path.isfile(os.path.join(resultDirectory,i)):
		exist.append(i)

datas = ReadDatas(dataDirectory)
for n in range(0, 200):
	fileName = (str(n) + ".csv")
	if fileName in exist:
		print("FileExist : " + fileName)
		continue	
	print("Calculating N = " + str(n))
	profitCurve = ProfitCurve(n, datas)
	print("Calculation Over, Writting file")
	resultPath = os.path.join(resultDirectory, fileName)
	file_object = open(resultPath, 'a')
	for key in profitCurve:
		file_object.write(str(key) + "," + str(profitCurve[key]) + "\r\n")
	print("save to file : " + resultPath)