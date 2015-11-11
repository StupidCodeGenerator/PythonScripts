from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import math
from scipy.interpolate import UnivariateSpline
import sys

fileName = sys.argv[1]

data = sp.genfromtxt(fileName, delimiter=",")

print(data[:10])

freq = {}

growth = []
for d in data:
	if not (sp.isnan(d[4]) or sp.isnan(d[1])):
		growth.append(d[4]/d[1])

params = norm.fit(growth)
print(params)