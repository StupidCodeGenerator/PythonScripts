from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline
import sys
import os
import copy
s = os.sep
root = sys.argv[1]

resultQuantity = {}
result = {}

# It will count how many raises before current step
def TotalRaiseBeforeNDays(data, currentDay, n):
	result = 0
	for i in range(currentDay - n, currentDay):
		result += math.log(data[i][4]/data[i][1])
	return result

def TotalRaiseAfterNDays(data, currentDay, n):
	result = 0
	for i in range(currentDay, currentDay + n):
		result += math.log(data[i][4]/data[i][1])
	return result

# It will fix the results above
def ProcessData(data):
	data = data[::-1]
	n = 20
	for i in range(n, len(data) - n):
		currentGrowth = TotalRaiseAfterNDays(data, i, n)
		totalRaise = TotalRaiseBeforeNDays(data, i, n)
		key = totalRaise
		if not (sp.isnan(key) or key == 0):
			if result.has_key(key):
				resultQuantity[key] += 1
				result[key] += currentGrowth
			else:
				resultQuantity[key] = 1
				result[key] = currentGrowth

########################################################################

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	ProcessData(data)
xs = sorted(result.keys())
ys = []
ys2 = []
for x in xs:
	ys.append(result[x] / resultQuantity[x])
	ys2.append(resultQuantity[x])

f, (ax1, ax2) = plt.subplots(2,1)
ax1.plot(xs, ys)
plt.title("Total growth in next 10 days and Data Density")
plt.xlabel("total raise in last 10 days")
ax2.plot(xs, ys2)
plt.show()