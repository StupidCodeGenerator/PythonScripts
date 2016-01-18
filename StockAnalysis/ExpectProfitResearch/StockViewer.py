from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from scipy.stats import lognorm
import matplotlib as mpl  
import sys
import os
s = os.sep

def FitPrice(data):
	priceData = data[:,6]
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
		return math.log(high/low);

fileName = sys.argv[1]
csvData = sp.genfromtxt(fileName, delimiter = ",")

HighLows = []
for i in range(0, len(csvData)):
	print("Calculating High/Low of " + str(i) + "/" + str(len(csvData)))
	subData = csvData[:i + 1]
	print("Sub length = " + str(len(subData)))
	highLow = HighLow(subData)
	print("Result["+str(i)+"] = " + str(highLow))
	HighLows.append(highLow)

y = csvData[:,6]
x = range(0, len(y))

line = [0 for col in range(len(HighLows))]

p1 = plt.subplot(211)
p2 = plt.subplot(212)
p1.plot(x, y)
p2.plot(range(0, len(HighLows)),HighLows)
p2.plot(range(0, len(HighLows)),line)
plt.show()
