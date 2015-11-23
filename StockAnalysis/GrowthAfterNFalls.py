# Growth After N Falls
# It will count the growth rate of M days after(contains) the day [i] 
# when there are N days of falls before [i]

from __future__ import division
import scipy as sp
import matplotlib.pyplot as plt
import math
import sys
import os

root = sys.argv[1]   # the data path

resultGrowth = {}    # Growt rate of given N days of raise
dataQuantity = {}    # the density of data

N = 10               # Count total growth of next N days

# It will count the Days of raise before that day
def ContinueFallsOfDays(data, currentDay):
	count = 0
	while currentDay > 0:
		currentDay -= 1
		if data[currentDay][4] / data[currentDay][1] < 1 :
			count += 1
		else:
			break;
	return count

# It will count the total growth rate after N days
def TotalGrowthAfterNDays(data, currentDay, n):
	growth = 0
	for i in range(currentDay, currentDay + n):
		growth += math.log(data[i][4]/data[i][1])
	return growth

# It will modify the results above
def ProcessData(data):
	data = data[::-1]
	for i in range(1, len(data) - N):
		currentGrowth = TotalGrowthAfterNDays(data, i, N)
		numOfFalls = ContinueFallsOfDays(data, i)
		if resultGrowth.has_key(numOfFalls):
			resultGrowth[numOfFalls] += currentGrowth
			dataQuantity[numOfFalls] += 1
		else:
			resultGrowth[numOfFalls] = currentGrowth
			dataQuantity[numOfFalls] = 1

########################################################################

# It will iterate all the files
for i in os.listdir(root):
    if os.path.isfile(os.path.join(root,i)):
    	print("Processing : " + i)
    	data = sp.genfromtxt(os.path.join(root,i), delimiter=",")
    	ProcessData(data)

xs = sorted(resultGrowth.keys())
ys = []
for x in xs:
	ys.append(resultGrowth[x] / dataQuantity[x])

plt.plot(xs, ys)
plt.grid()
plt.xlabel("NumOfFalls")
plt.ylabel("E(Sigma(ln(p[n]/p[n-1])))")
plt.show()