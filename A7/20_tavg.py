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
#------------------------------------------------------------------------------------------------
data = read_data('Rg.out.20.3')
ydata = [row[1] for row in data]
t = tau(ydata)
xdata = [row[0] for row in data]
print(t)
plt.figure(figsize=(12, 4.8))
plt.scatter(xdata, ydata, s = 4.0, label = 'Data for 7th ensemble for N = 20')
plt.plot([0, 300000], [ydata[int(t/1000)]]*2, 'r', label = r'$R_g $ value at $t = \tau$')
plt.xlabel(r'Timesteps $\longrightarrow$')
plt.ylabel(r'$R_g \longrightarrow$')
plt.title("Visualizing time average for the 3rd ensemble of N = 20 system")
plt.legend()
plt.axvspan(t, 300000, facecolor='b', alpha=0.1) # colors the background, alpha is transparency
plt.savefig('Q3_A7.png', dpi=300, bbox_inches='tight')
tavg = np.mean(np.array([row[1] for row in data[int(t/1000):]]))
print("Time average is " + str(tavg))