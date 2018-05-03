__author__ = 'weiweiduan'
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 5, 10)   #Return 10 evenly spaced numbers between 0 and 5
y = x * x
fig, ax = plt.subplots()    #a figure and a grid of subplot
ax.plot(x, y)   #plot the points on the grid
plt.show()  #show the graph
