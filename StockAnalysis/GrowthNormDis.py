﻿from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import math
from scipy.interpolate import UnivariateSpline
import sys
import os

root = sys.argv[1]
growth = []

for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
		print("Processing" + str(i))
		data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
		for d in data:
			if not (sp.isnan(d[4]) or sp.isnan(d[1])):
				value = d[4]/d[1]
				if value >= 0.9 and value <= 1.1:
					growth.append(value)

params = norm.fit(growth)
print(params)

plt.hist(growth, bins=100, normed=True, alpha=0.6, color='g')
xmin, xmax = plt.xlim()
x = np.linspace(xmin, xmax, 100)
p = norm.pdf(x, params[0], params[1])
plt.plot(x, p)
plt.show()