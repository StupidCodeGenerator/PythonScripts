from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import matplotlib as mpl  
import sys
import os
s = os.sep

fileName = sys.argv[1]
csvData = sp.genfromtxt(fileName, delimiter = ",")

y = csvData[:,4]
x = range(0, len(csvData))

plt.plot(x, y)
plt.show()