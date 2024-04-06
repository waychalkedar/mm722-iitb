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
def exp(x, a, b):
    return a * np.power(x, b) 

eavg = []
length  = [20, 30, 40, 50, 100]
for l in length:
    t = 0
    s = ''
    if l == 50 or l == 100:
        s = 'long'
        temp = np.zeros((10, 601))
    else:
        temp = np.zeros((10, 301))
    for e in range(1, 11, 1):
        data = read_data('Rg.out{}.{}.{}'.format(s, l, e))
        temp[e-1] = [row[1] for row in data]
        if l == 40 and e == 2:
            t = tau([row[1] for row in data])
        if l != 40 and e == 3:
            t = tau([row[1] for row in data])
    eavg.append(np.average([row[5*int(t/1000)] for row in temp]))
plt.loglog(length, eavg, 'o', label = 'Ensemble-average')

popt, pcov = curve_fit(exp, length, eavg)

# popt, pcov = curve_fit(lin, length, eavg)
plt.loglog(length, exp(length, *popt), 'r', label = 'log $R_g$ = {} log $N$ + {}'.format(0.4931,0.4351))
plt.title("Visualizing variation of ensemble-average with system size")
plt.xlabel(r'Size of polymer $N \longrightarrow$')
plt.ylabel(r'Average $R_g \longrightarrow$')
plt.legend()
# plt.savefig("Q5_A7.png", dpi=300, bbox_inches='tight')
plt.show()