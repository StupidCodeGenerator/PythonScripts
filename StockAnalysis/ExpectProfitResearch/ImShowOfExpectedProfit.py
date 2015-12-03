# the X is days between buy-in and sell 
# the Y is the buy-in price
# So the graph is about the Expected profit by given buy-in price and N days later sell.
from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
import matplotlib as mpl  
import sys
import os
s = os.sep

# Read the csv and make them into 2d data set
# The only problem is that each csv's length is different
# So I need a standard of the buy-in price.

# I will make the buyin price's range from 0 to 5. higher
# values is not that necessary.
# then use (price / 0.05) to find out the index.
# The length will be 5/0.05 = 100 indecies
# To avoid null values, init the 2d array with 0 first

def LoadData(filePath):
	result = []
	for i in range(0, 150):
		result.append(0)
	print("LOADING : " + filePath)
	csvData = sp.genfromtxt(filePath, delimiter = ",")
	for row in csvData:
		# int(3.0) == 2 because the int() is losting data
		index = int(row[0]/0.05 + 0.1) 
		if index >= 0 and index < len(result):
			result[index] = row[1]
	return result

# START
# -----------------------------------------------------------------------------
dataDirectory = sys.argv[1]
data = {}

for i in os.listdir(dataDirectory):
	key = int(i.split(".")[0])   # get *** from ***.csv
	fullPath = os.path.join(dataDirectory, i)
	if os.path.isfile(fullPath):
		data[key] = LoadData(fullPath)

dataArray = []
for key in sorted(data):
	dataArray.append(data[key])

im = plt.imshow(dataArray, vmin = -1, vmax = 1)
plt.colorbar(im)
ax=plt.gca()
ax.set_xticklabels(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))
plt.show()  