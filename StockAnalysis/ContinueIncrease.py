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

data = []

for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("opening file : " + i)
    	fileContent = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	for d in fileContent:
    		data.append(d);

growth = []

for d in data:
	value = d[4]/d[1]
	if not sp.isnan(value):
		growth.append(value)

def GetSubGrowth(grow, numOfInc):
	sub = []
	for i in range(numOfInc, len(grow)):
		cond = True
		for j in range(1,numOfInc + 1):
			if grow[i-j] < 1:
				cond = False;
		if cond :
			sub.append(growth[i])
	return sub

def GetIncProbAndDecProb(grow):
	numOfInc = 0
	numOfDec = 0
	for g in grow:
		if g > 1:
			numOfInc += 1
		elif g < 1:
			numOfDec += 1
	return numOfInc/len(grow), numOfDec/len(grow)

increaseProb = []
decreaseProb = []
for i in range(1, 20):
	print("Calculating sub of " + str(i))
	sub = GetSubGrowth(growth, i)
	param = GetIncProbAndDecProb(sub)
	increaseProb.append(param[0])
	decreaseProb.append(param[1])

plt.grid()
plt.plot(range(1, len(increaseProb) + 1), increaseProb)
plt.plot(range(1, len(decreaseProb) + 1), decreaseProb)
plt.show()