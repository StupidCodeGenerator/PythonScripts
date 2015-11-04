from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
import math
from scipy.interpolate import UnivariateSpline

def EntropyCalculation(priceData):
	histogram = np.histogram(priceData, bins=100, normed=True)
	entropy = 0
	for d in histogram[0]:
		if(d != 0):
			entropy += d * math.log(1/d)
	return entropy

data = sp.genfromtxt("D:/StockData/data/000001.csv", delimiter=",")
priceDataAll = data[:, 1]
priceDataAll = priceDataAll[~sp.isnan(priceDataAll)]

entropies = []
for i in range(0, 3000):
	cuttedData = priceDataAll[i:]
	entropies.append(EntropyCalculation(cuttedData))

plt.plot(range(0,len(entropies)), entropies)
plt.show()