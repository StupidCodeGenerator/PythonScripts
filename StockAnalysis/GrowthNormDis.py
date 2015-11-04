﻿from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline

data = sp.genfromtxt("data/000001.csv", delimiter=",")

freq = {}

priceData = data[:, 7]

priceData = priceData[~sp.isnan(priceData)]

histogram = np.histogram(priceData, bins=100, normed=True)

# Plot the histogram.
plt.hist(priceData, bins=50, normed=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 50)
p = norm.pdf(x, mu, std)
plt.plot(x, p, 'k', linewidth=2)
title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
plt.title(title)

plt.show()