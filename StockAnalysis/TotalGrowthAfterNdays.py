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

result = []
# It will count how many raises before current step
def TotalGrowthAfterNDays(data, currentDay, n):
	result = 0
	for i in range(currentDay, currentDay + n):
		result += math.log(data[i][4]/data[i][1])
	return result

# It will fix the results above
def ProcessData(data):
	data = data[::-1]
	n = sys.argv[2]
	for i in range(0, len(data) - n):
		totalGrowth = TotalGrowthAfterNDays(data, i, n)
		result.append(totalGrowth)

########################################################################

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	ProcessData(data)

plt.title("TotalRaiseAfter10Days_Distribution")
plt.hist(result, bins=100, normed=True)
plt.show()