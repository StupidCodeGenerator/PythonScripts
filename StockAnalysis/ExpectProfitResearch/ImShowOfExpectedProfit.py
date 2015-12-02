# the X is days between buy-in and sell 
# the Y is the buy-in price
# So the graph is about the Expected profit by given buy-in price and N days later sell.
from __future__ import division
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from scipy.stats import lognorm
from matplotlib import mpl  

# Read the csv and make them into 2d data set
# The only problem is that each csv's length is different
# So I need a standard of the buy-in price.

# Below this line is codes from internet
# ------------------------------------------------------

data=np.clip(np.random.randn(20,5),-1,1)

print(data)

im = plt.imshow(data, extent = (0,5,0,5))
plt.colorbar(im)
ax=plt.gca()
ax.set_yticks(np.linspace(0,5,20))
  
plt.show()  