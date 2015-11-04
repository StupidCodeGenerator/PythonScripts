from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import math
from scipy.interpolate import UnivariateSpline

data = sp.genfromtxt("data/000001.csv", delimiter=",")

freq = {}

priceData = data[:, 1]

priceData = priceData[~sp.isnan(priceData)]

shape, loc, scale = lognorm.fit(priceData)

plt.hist(priceData, bins=100, normed=True, alpha=0.6, color='g')
#plt.scatter(range(0, len(priceData)), priceData)
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = lognorm.pdf(x, shape, loc, scale)
#plt.plot(x, p, 'k', linewidth=2)
plt.title("Price Hist")
plt.show()