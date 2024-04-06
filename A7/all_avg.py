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
#------------------------------------------------------------------------------
length  = [20, 30, 40, 50, 100]
for l in length: # loops over all systems
    tavg = 0
    eavg = 0
    t = 0
    s = ''
    if l == 50 or l == 100: # this is so we read data from the long simulation for N = 50, 100
        s = 'long'
        temp = np.zeros((10, 601)) 
    else:
        temp = np.zeros((10, 301))
    for e in range(1, 11, 1):
        data = read_data('Rg.out{}.{}.{}'.format(s, l, e))
        temp[e-1] = [row[1] for row in data]
        if l == 40 and e == 2: # ensemble 3 fro N = 40 gave wildly incorrect results, so ensemble 2 is chosen only for N = 40
            t = tau([row[1] for row in data])
            tavg = np.mean(np.array([row[1] for row in data[int(t/1000):]]))
        if l != 40 and e == 3: # for all other polymer lengths, ensemble 3 is taken to compute time-average
            t = tau([row[1] for row in data])
            tavg = np.mean(np.array([row[1] for row in data[int(t/1000):]]))
    eavg = np.average([row[5*int(t/1000)] for row in temp])
    plt.plot(l, tavg, 'o', c='r')
    plt.plot(l, eavg, 'o', c='g')
plt.title("Comparision of time-averages and ensemble-averages")
plt.xlabel(r'Size of polymer $N$')
plt.ylabel(r'Average $R_g \longrightarrow$')
plt.legend(["Time-average","Ensemble-average"])
# plt.savefig("Q4_A7.png", dpi=300, bbox_inches='tight')
plt.show()