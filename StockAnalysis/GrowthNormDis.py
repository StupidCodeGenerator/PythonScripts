from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline

import os
s = os.sep
root = "./data/"

data = []

for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	fileContent = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	for d in fileContent:
    		data.append(d);

growth = []

for d in data:
	value = d[4]/d[1]
	if not sp.isnan(value):
		growth.append(value)

print(growth[0])

subGrowth = []
for i in range(3, len(growth)):
	if growth[i - 1] > 1 and growth[i - 2] > 1 and growth[i - 3] > 1:
		subGrowth.append(growth[i])

plt.hist(subGrowth, bins=100, normed=True, alpha=0.6, color='g')
plt.grid()
plt.show()