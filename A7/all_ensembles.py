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
# ------------------------------------------------------------------------------------------------------------------------
files = []
for length in [20, 30, 40, 50, 100]:
    plt.figure(figsize=(12, 4.8))
    for ens in range(1, 11, 1):
        data = read_data('Rg.out.{}.{}'.format(length, ens))
        plt.plot([row[0] for row in data], [row[1] for row in data], label = 'Ensemble {}'.format(ens), linewidth = 1.0)
    plt.title('Combined ensemble plots for radius of gyration vs time for polymer length = ' + str(length))
    plt.xlabel(r'Timesteps $\longrightarrow$')
    plt.ylabel(r'$R_g \longrightarrow$')
    plt.legend(loc='upper right', ncols=5)
    # plt.savefig('A7_plots_{}.png'.format(length), dpi=300, bbox_inches='tight')
    plt.show()

# since the system doesn't seem to have equilibrated for a long enough time for N = 50, 100, we run them for longer 
# and see how the systems evolve
for l in [50, 100]:
    plt.figure(figsize=(12, 4.8))
    for e in range(1, 11, 1):
        data = read_data('Rg.outlong.{}.{}'.format(l, e))
        plt.plot([row[0] for row in data], [row[1] for row in data], label = 'Ensemble {}'.format(e), linewidth = 1.0)
    plt.title('Combined ensemble plots for radius of gyration vs time for polymer length = ' + str(l) + ' for a longer equilibration')
    plt.xlabel(r'Timesteps $\longrightarrow$')
    plt.ylabel(r'$R_g \longrightarrow$')
    plt.legend(loc='upper right', ncols=5)
    # plt.savefig('A7_longplots_' + str(l), dpi = 300, bbox_inches='tight')
    plt.show()
