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

# Final result
# key : PM // 0.2 * 0.2
# value : Num of raises
result = {}

totalGrowth = []

# It will return the stock's most possible price
def MostProbPrice(data):
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


# It will fix the results above
def ProcessData(data):
	growthOfThisData = 0
	mostProbPrice = MostProbPrice(data)
	if mostProbPrice == 0:
		return
	print("FitResult : " + str(mostProbPrice))	
	for i in range(0, len(data)):
		if not (sp.isnan(data[i][1]) or sp.isnan(data[i][4])):
			if data[i][1] > 0:
				currentGrowth = data[i][4] / data[i][1]
				growthOfThisData += math.log(currentGrowth)
				pm = data[i][4] / mostProbPrice
				key = (pm // 0.05) * 0.05
				if result.has_key(key):
					result[key] += math.log(currentGrowth)
				else:
					result[key] = math.log(currentGrowth)
	print("GrowthRate:" + str(growthOfThisData))
	totalGrowth.append(growthOfThisData)

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
	resultY.append(result[key])
plt.title("Average GrowthRate = " + str(sum(totalGrowth) / len(totalGrowth)))
plt.grid()
plt.plot(resultX, resultY)
plt.xlabel("CurrentPrice / FitPrice")
plt.ylabel("Sigma(ln(GrowthRate))")
plt.show()