from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import interpolate 
import sys
import os

stockData = sp.genfromtxt(sys.argv[1], delimiter=",")

y = stockData[:,6]
x = range(0, len(y))

x_new = np.linspace(0, len(x) - 1, 100)
f_linear = interpolate.interp1d(x, y)

plt.plot(x, y, label = "oridata")
plt.plot(x_new, f_linear(x_new), label="linspace")
plt.show()