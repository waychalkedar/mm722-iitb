import numpy as np
import matplotlib.pyplot as plt
import re, yaml
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from scipy.optimize import curve_fit
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader

# From ChatGPT
def read_data(filename):
    data_matrix = []
    with open(filename, 'r') as file:
        # Skip the first two lines
        next(file)
        next(file)
        # Read data from the third line onwards
        for line in file:
            # Split the line into individual elements
            elements = line.strip().split()
            # Convert elements to integers or floats as appropriate
            row = [int(element) if element.isdigit() else float(element) for element in elements]
            data_matrix.append(row)
    return data_matrix

def func(x, a, b, c):
    return a*np.exp(b*x) + c

# tau is a function which estimates time constant by returning the timestep at which the curve hits/crosses a y-value of
# 0.37 * y_max (since for an exponential decay y = Ae^(-t/tau), t = tau gives y = 0.37 * A or 0.37 * y_max
def tau(y):
    t = 0
    for k in range(len(y)-1):
        if np.round(y[k], 4) < np.round(0.37*y[0], 4) and np.round(y[k+1], 4) > np.round(0.37*y[0], 4):
            t = data[k][0]
            break
    return t
# -------------------------------------------------------------------------------------------------------------------------------
# to evaluate timestep, take mean of curves
temp = np.zeros((10, 301))
for ens in range(1, 11, 1):
    data = read_data('Rg.out.20.{}'.format(ens))
    temp[ens-1] = [row[1] for row in data] # extracts only the column for R_g, stores it into a matrix for different ensembles
ydata = np.average(temp, axis=0)
xdata = np.array([row[0] for row in data])
t = tau(ydata)
print(r'Estimated time constant is {} timesteps'.format(t))

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4.8))
fig.suptitle('Estimating the time constant for $R_g$ vs timesteps for N = 20')
ax1.scatter(xdata, ydata, s = 4.0, label = 'Average curve for $R_g$ vs timesteps')
ax1.plot([0, 300000], [0.37*ydata[0]]*2, 'r', label = r'$R_g = 0.37 \times R_{g,max}$') # plots y = 0.37 * y_max
ax1.set(xlabel = r'Timesteps $\longrightarrow$', ylabel = r'$R_g \longrightarrow$')
ax1.legend(markerscale = 2.0)
ax2.scatter(xdata, ydata, s = 4.0, label = 'Average curve for $R_g$ vs timesteps')
ax2.plot([0, 300000], [0.37*ydata[0]]*2, 'r', label = r'$R_g = 0.37 \times R_{g,max}$')
# ax2.plot([0, 300000], [np.mean(ydata[int(t/1000):])]*2)
ax2.set_ylim(1.5, 2.5)
ax2.legend(markerscale = 2.0)
ax2.set(xlabel = r'Timesteps $\longrightarrow$', ylabel = r'$R_g \longrightarrow$')
# fig.savefig('Q1_A7_estimating_time.png', dpi = 300, bbox_inches='tight')
ensavg = np.mean([row[5*int(t/1000)] for row in temp])
print(r'Ensemble average of is {}'.format(ensavg))