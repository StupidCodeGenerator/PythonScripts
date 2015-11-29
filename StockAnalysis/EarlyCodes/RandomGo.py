from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import math
import random
from scipy.interpolate import UnivariateSpline

growth = norm.rvs(loc=1, scale=0.023, size=1000)
path = []
startValue = 10
for g in growth:
	startValue = startValue * g
	path.append(startValue)

f, (ax1, ax2) = plt.subplots(2,1)
ax1.hist(growth, bins=30, normed=True, alpha=0.6, color='g')
ax2.plot(range(0, len(path)), path)
plt.grid()
plt.show()