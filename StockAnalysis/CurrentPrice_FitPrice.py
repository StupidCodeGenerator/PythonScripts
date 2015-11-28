# The relationship between (currentPrice/fitPrice) and Avr(MaxPrice in Next N Days)
# and Avr(MinPrice in Next N Days)

from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline
import sys
import os
import copy
s = os.sep
root = sys.argv[1]

# the KeyOfData is (TotalRaise in last N days) // 0.02 * 0.02
# KeyOfData / how many datas of that key
numOfDataMax = {}
numOfDataMin = {}
# KeyOfData / sum of value
maxPriceResult = {}
minPriceResult = {}

# It will return the stock's most possible price
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

def TotalRaiseAfterNDays(data, currentDay, n):
	result = 0
	for i in range(currentDay, currentDay + n):
		result += math.log(data[i][4]/data[i][1])
	return result

def MaxPriceInNextNDays(data, currentDay, n, fitPrice):
	result = 0
	for i in range(currentDay, currentDay + n):
		value = data[i][4] / fitPrice - data[currentDay][4]/fitPrice
		if value > result:
			result = value
	return result

def MinPriceInNextNDays(data, currentDay, n, fitPrice):
	result = 65535
	for i in range(currentDay, currentDay + n):
		value = data[i][4] / fitPrice - data[currentDay][4]/fitPrice
		if value < result:
			result = value
	return result

# It will fix the results above
def ProcessData(data):
	data = data[::-1]
	n = 100
	growthOfThisData = 0
	fitPrice = FitPrice(data)
	if fitPrice == 0:
		return
	print("FitResult : " + str(fitPrice))	
	for i in range(0, len(data) - n):
		if not (sp.isnan(data[i][1]) or sp.isnan(data[i][4]) or sp.isnan(data[i][5])):
			if data[i][5] > 0:
				maxPrice = MaxPriceInNextNDays(data, i, n, fitPrice)
				minPrice = MinPriceInNextNDays(data, i, n, fitPrice)
				currentPrice = data[i][4] / fitPrice
				key = (currentPrice // 0.05) * 0.05
				if maxPriceResult.has_key(key):
					maxPriceResult[key] += maxPrice
					numOfDataMax[key] += 1
				else:
					maxPriceResult[key] = maxPrice
					numOfDataMax[key] = 1
				if minPriceResult.has_key(key):
					minPriceResult[key] += minPrice
					numOfDataMin[key] += 1
				else:
					minPriceResult[key] = minPrice
					numOfDataMin[key] = 1

########################################################################

# It will iterate all the files
for i in os.listdir(root):
	if os.path.isfile(os.path.join(root,i)):
		print("Processing : " + i)
		data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
		ProcessData(data)

print(minPriceResult)

resultXMax = []
resultYMax = []
resultXMin = []
resultYMin = []
for key in sorted(maxPriceResult):
	resultXMax.append(key)
	resultYMax.append(maxPriceResult[key] / numOfDataMax[key])
for key in sorted(minPriceResult):
	resultXMin.append(key)
	resultYMin.append(minPriceResult[key] / numOfDataMin[key])
plt.grid()
fig = plt.figure() 
ax1 = fig.add_subplot(2,1,1,xlim=(0, 2), ylim=(0, 2))
ax1.plot(resultXMax, resultYMax)
ax2 = fig.add_subplot(2,1,2,xlim=(0, 2), ylim=(-2, 0))
ax2.plot(resultXMin, resultYMin)
plt.xlabel("CurrentPrice / FitPrice")
plt.show()