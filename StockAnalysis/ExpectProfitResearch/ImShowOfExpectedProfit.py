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
stockData = [] # Element will be array of each N

def LoadData(filePath):
	result = []
	for i in range(0, 100):
		result.append(0)
	print("LOADING : " + filePath)
	csvData = sp.genfromtxt(filePath, delimiter = ",")
	for row in csvData:
		index = int(row[0]//0.05)
		if index > 0 and index < len(result):
			result[index] = row[1]
	return result

# START
# -----------------------------------------------------------------------------
dataDirectory = sys.argv[1]
data = []

for i in os.listdir(dataDirectory):
	fullPath = os.path.join(dataDirectory, i)
	if os.path.isfile(fullPath):
		data.append(LoadData(fullPath))


# Below this line is codes from internet
# -----------------------------------------------------------------------------
im = plt.imshow(data)
plt.colorbar(im)
#ax=plt.gca()
#ax.set_yticks(np.linspace(0,5,20))
#ax.set_yticklabels(("0","0.25","0.5","0.75","1",\
#	"1.25", "1.5", "1.75", "2", "2.25", "2.5", "2.75", "3", \
#	"3.25", "3.5", "3.75", "4", "4.25", "4.5", "4.75", "5"))
#  
plt.show()  