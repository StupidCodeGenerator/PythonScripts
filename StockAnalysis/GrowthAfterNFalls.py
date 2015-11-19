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

# final results
resultGrowth = {}
dataQuantity = {}
# It will count how many raises before current step
def ContinueFallOfDays(data, currentStep):
	count = 0
	while currentStep > 0:
		currentStep -= 1
		if data[currentStep][4] / data[currentStep][1] < 1 :
			count += 1
		else:
			break;
	return count

# It will fix the results above
def ProcessData(data):
	data = data[::-1]
	for i in range(1, len(data)):
		currentGrowth = math.log(data[i][4] / data[i][1])
		numOfFallBefore = ContinueFallOfDays(data, i)
		if resultGrowth.has_key(numOfFallBefore):
			resultGrowth[numOfFallBefore] += currentGrowth
			dataQuantity[numOfFallBefore] += 1
		else:
			resultGrowth[numOfFallBefore] = currentGrowth
			dataQuantity[numOfFallBefore] = 1

########################################################################

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	ProcessData(data)

xs = sorted(resultGrowth.keys())
ys = []
for x in xs:
	ys.append(resultGrowth[x] / dataQuantity[x])

plt.plot(xs, ys)
plt.grid()
plt.xlabel("NumOfFalls")
plt.ylabel("Avr(ln(p[n]/p[n-1]))")
plt.show()