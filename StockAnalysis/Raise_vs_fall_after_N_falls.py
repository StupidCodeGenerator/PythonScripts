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
resultRaises = {}
resultFalls = {}
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
	# clean data
	nans = []
	for i in range(0, len(data)):
		if sp.isnan(data[i][1]) or sp.isnan(data[i][4]):
			nans.append(i)

	#data = np.delete(data, nans)
	data = data[::-1]
	for i in range(1, len(data)):
		currentGrowth = data[i][4] / data[i][1]
		numOfRaisesBefore = ContinueFallOfDays(data, i)
		if currentGrowth > 1:
			if resultRaises.has_key(numOfRaisesBefore):
				resultRaises[numOfRaisesBefore] += 1
			else:
				resultRaises[numOfRaisesBefore] = 1
		elif currentGrowth < 1:
			if resultFalls.has_key(numOfRaisesBefore):
				resultFalls[numOfRaisesBefore] += 1
			else:
				resultFalls[numOfRaisesBefore] = 1

########################################################################

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	ProcessData(data)

for key in copy.copy(resultRaises):
	if not resultFalls.has_key(key):
		resultRaises.pop(key)
for key in copy.copy(resultFalls):
	if not resultRaises.has_key(key):
		resultFalls.pop(key)

print(resultRaises)
print(resultFalls)

xs = sorted(resultRaises.keys())
ys = []
for x in xs:
	ys.append(resultRaises[x]/resultFalls[x])

plt.plot(xs, ys)
plt.grid()
plt.show()