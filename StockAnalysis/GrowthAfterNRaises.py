# Growth After N Raise
# It will count the growth rate of M days after(contains) the day [i] 
# when there are N days of raise before [i]

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

# It will count how many raises before current step
def ContinueRaiseOfDays(data, currentStep):
	count = 0
	while currentStep > 0:
		currentStep -= 1
		if data[currentStep][4] / data[currentStep][1] > 1 :
			count += 1
		else:
			break;
	return count

# It will count how many raises before current step
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
		numOfRaisesBefore = ContinueRaiseOfDays(data, i)
		if resultGrowth.has_key(numOfRaisesBefore):
			resultGrowth[numOfRaisesBefore] += currentGrowth
			dataQuantity[numOfRaisesBefore] += 1
		else:
			resultGrowth[numOfRaisesBefore] = currentGrowth
			dataQuantity[numOfRaisesBefore] = 1

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
plt.xlabel("NumOfRaises")
plt.ylabel("Avr(ln(p[n]/p[n-1]))")
plt.show()