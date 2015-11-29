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

# The actual price, has noting to do with FitPrice and CurrentPrice
def ExpectedPriceAfterNDays(data, currentDay, n):
	return data[currentDay + n - 1][4]  # Give the last day's price

dataQuantities = {}
result = {}
# This function will write the result to dicts above
def ProcessData(data):
	data = data[::-1]  # The data I got from internet is from now to past.
	n = 100
	growthOfThisData = 0
	fitPrice = FitPrice(data)
	if fitPrice == 0:
		return
	print("FitResult : " + str(fitPrice))
	for i in range(0, len(data) - n):
		if not (sp.isnan(data[i][1]) or sp.isnan(data[i][4]) or sp.isnan(data[i][5])):
			if data[i][5] > 0: # Avoid the days that stops dealing
				maxPossiblePriceAfterNDays = ExpectedPriceAfterNDays(data, i, n) / fitPrice
				currentPrice = data[i][4] / fitPrice  
				key = (currentPrice // 0.05) * 0.05                 # granulate current price
				value = maxPossiblePriceAfterNDays - currentPrice   # expect growth
				if result.has_key(key):
					result[key] += value
					dataQuantities[key] += 1
				else:
					result[key] = value
					dataQuantities[key] = 1

# START
########################################################################

# It will iterate all the files
for i in os.listdir(root):
	if os.path.isfile(os.path.join(root,i)):
		print("Processing : " + i)
		data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
		ProcessData(data)

resultX = []
resultY = []
for key in sorted(result):
	resultX.append(key)
	resultY.append(result[key] / dataQuantities[key])
plt.grid()
plt.plot(resultX, resultY)
plt.ylabel("Expect Profit ( of Relative Price )")
plt.xlabel("Current Relative Price")
plt.show()