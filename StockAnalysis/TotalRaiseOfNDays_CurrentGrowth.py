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
def TotalRaiseOfNDays(data, currentDay, n):
	result = 0
	for i in range(currentDay - n, currentDay):
		result += math.log(data[i][4]/data[i][1])
	return result

# It will fix the results above
def ProcessData(data):
	data = data[::-1]
	n = 10
	for i in range(n, len(data)):
		currentGrowth = math.log(data[i][4] / data[i][1])
		totalRaise = TotalRaiseOfNDays(data, i, n)
		key = currentGrowth // 0.01 * 0.01
		if not sp.isnan(key):
			if result.has_key(key):
				resultQuantity[key] += 1
				result[key] += totalRaise
			else:
				resultQuantity[key] = 1
				result[key] = totalRaise

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
ax2.plot(resultQuantity, xs)
plt.show()