from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy import interpolate 
import sys
import os

stockData = sp.genfromtxt(sys.argv[1], delimiter=",")

priceData = stockData[:,6]

def MovingAverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array

def ExpMovingAverage(values, window):
    weights = np.exp(np.linspace(-1., 0., window))
    weights /= weights.sum()
    a =  np.convolve(values, weights, mode='full')[:len(values)]
    a[:window] = a[window]
    return a

def MACD(x, slow=26, fast=12):
    emaslow = ExpMovingAverage(x, slow)
    emafast = ExpMovingAverage(x, fast)
    return emaslow, emafast, emafast - emaslow

macd = MACD(priceData)

plt.plot(range(0, len(priceData)), priceData, label = "price")
plt.plot(range(0, len(macd[0])), macd[0], label = "macd1")
plt.plot(range(0, len(macd[1])), macd[1], label = "macd2")
plt.plot(range(0, len(macd[2])), macd[2], label = "macd3")
plt.grid()
plt.legend()
plt.show()