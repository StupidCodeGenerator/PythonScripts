from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline
import sys
import os
s = os.sep
root = sys.argv[1]

def ContinueRaiseOfDays(data, today):
	if today == 0:
		return 0
	# TODO : count the raises

# It will return the num of Raise and Fall by given last 10 day's growth rate
def GetIncDecNums(data, growthRate):
	numOfIncrease = 0
	numOfDecrease = 0
	for i in range(11, len(data)):
		value = data[i-1][4]/data[i-11][4]
		if not sp.isnan(value) and value > growthRate:
			currentGrowth = data[i][4]/data[i][1]
			if currentGrowth > 1:
				numOfIncrease += 1
			elif currentGrowth < 1:
				numOfDecrease += 1
	return numOfIncrease, numOfDecrease

# it will return 2 maps, the key is the growth rate of last 10 days.
# Value of 1st result is numOfRaises, Value of 2nd is numOfFalls
def ProcessData(data):
	increaseResult = {}
	decreaseResult = {}
	data = data[::-1]
	for i in range(0, 60):
		growthRate = 1 + (i/20)
		params = GetIncDecNums(data, 1 + (i/20))
		increaseResult[growthRate] = params[0]
		decreaseResult[growthRate] = params[1]
	return increaseResult, decreaseResult

#############################################################################

# The key is the growth rate of last 10 days, the value is 
# (num of Increase) / (num of Decrease)
resultIncrease = {}
resultDecrease = {}

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	d = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	dataResult = ProcessData(d)
    	for key in dataResult[0]:
    		if resultIncrease.has_key(key):
    			resultIncrease[key] += dataResult[0][key]
    		else:
    			resultIncrease[key] = dataResult[0][key]
    	for key in dataResult[1]:
    		if resultDecrease.has_key(key):
    			resultDecrease[key] += dataResult[1][key]
    		else:
    			resultDecrease[key] = dataResult[1][key]
	print(resultIncrease)
	print(resultDecrease)

xs = sorted(resultIncrease.keys())
ys = []
for x in xs:
	ys.append(resultIncrease[x]/resultDecrease[x])

plt.plot(xs, ys)
plt.show()