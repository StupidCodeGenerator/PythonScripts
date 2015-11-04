from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

data = sp.genfromtxt("data/000002.csv", delimiter=",")
priceDataAll = data[:, 1]
priceDataAll = priceDataAll[~sp.isnan(priceDataAll)]

priceDatas = []

for i in range(0, len(priceDataAll) - 1):
	listIndex = i // 200
	subIndex = i % 200
	if(len(priceDatas) <= listIndex):
		priceDatas.append([])
	priceDatas[listIndex].append(priceDataAll[i])

avrs = []

for priceData in priceDatas:
	avr = sum(priceData) / len(priceData)
	avrs.append(avr)

plt.plot(range(0, len(avrs)), avrs)
plt.title("Avr plot")
plt.xlabel("index * 200days")
plt.ylabel("AvrPrice")
plt.grid()
plt.show()
