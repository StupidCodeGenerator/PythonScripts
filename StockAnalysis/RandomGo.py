from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.stats import lognorm
import math
import random
from scipy.interpolate import UnivariateSpline

randomData = []

for index in range(0,3):
	value = 10
	subRandom = []
	for i in range(0, 1000):
		r = random.random()
		r = 1.1 - r/5
		value = value * r
		subRandom.append(value)
	randomData.append(subRandom)

plt.title("StartValue = 10")
for index in range(0,len(randomData)):
	plt.plot(range(0, len(randomData[index])), randomData[index])
plt.show()