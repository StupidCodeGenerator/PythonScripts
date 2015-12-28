from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
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

fileName = sys.argv[1]
csvData = sp.genfromtxt(fileName, delimiter = ",")

FitPrice_History = []
for i in range(0, len(csvData)):
	print("Calculating fitPrice of " + str(i) + "/" + str(len(csvData)))
	subData = csvData[:i + 1]
	print("Sub length = " + str(len(subData)))
	fitPrice = FitPrice(subData)
	print("Result["+str(i)+"] = " + str(fitPrice))
	FitPrice_History.append(fitPrice)

y = csvData[:,6]
x = range(0, len(csvData))

plt.plot(x, y, label = "Price")
plt.plot(range(0, len(FitPrice_History)),FitPrice_History, label = "Fit")
plt.legend()
plt.show()
