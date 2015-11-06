from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
import math
from scipy.interpolate import UnivariateSpline

data = sp.genfromtxt("data/000001.csv", delimiter=",")

freq = {}

priceDataOri = data[:, 6]

priceDataOri = priceDataOri[~sp.isnan(priceDataOri)]

growth = []

for i in range(1, len(priceDataOri)):
	g = math.log(priceDataOri[i]/priceDataOri[i-1])
	if(g < math.log(1.1) and g > math.log(0.9)):
		growth.append(g)

histogram = np.histogram(growth, bins=100, normed=True)

# Plot the histogram.
plt.hist(growth, bins=50, normed=True, alpha=0.6, color='g')

# Plot the PDF.
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 50)
#p = norm.pdf(x, mu, std)
#plt.plot(x, p, 'k', linewidth=2)
#title = "Fit results: mu = %.2f,  std = %.2f" % (mu, std)
#plt.title(title)

plt.show()