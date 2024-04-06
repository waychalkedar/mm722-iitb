import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader
import warnings
warnings.simplefilter(action='ignore', category=[FutureWarning, DeprecationWarning])
# from https://stackoverflow.com/questions/32470543/open-file-in-another-directory-python
from pathlib import Path
import os
from scipy.optimize import curve_fit
from adjustText import adjust_text

def line(x, m):
    return m * x 

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

def thermo(file):
    docs = ""
    thermo = []
    with open(file, "r") as f:
        for line in f:
            m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
            if m: docs += m.group(0) + '\n'
    thermo = np.array(list(yaml.load_all(docs, Loader=Loader)))
    return thermo

def dump(file):
    temp = [] 
    with open(file, "r") as f:
            temp = np.array(list(yaml.load_all(f, Loader=Loader)))
    return temp
# -----------------------------------------------------------------------------------------
i = 0
d = np.zeros(6)
# for n1 in [0, 2625, 5250, 7875, 10500, 13125]:
plt.figure(figsize=(9.6, 4.8))
for n1 in [0, 2625, 5250, 7875, 10500, 13125]:
    msd1 = read_data("msd_atom1_n1={}.txt".format(n1))
    msd2 = read_data("msd_atom2_n1={}.txt".format(n1))
    x = [int(row[0]) for row in msd1]
    y1 = [row[1] for row in msd1]
    y2 = [row[1] for row in msd2]
    popt1, pcov1 = curve_fit(line, x, y1)
    popt2, pcov2 = curve_fit(line, x, y2)
    if n1 == 0:
        plt.plot(x, line(np.array(x), *popt2), label = "$n_2={}$".format(1.0 - n1/13125))
        i += 1
        continue
    plt.plot(x, line(np.array(x), *popt1), label = "$n_2={}$".format(1.0 - n1/13125))
    i += 1
plt.title("Comparision of fitted MSD vs time across systems")
plt.xlabel("Time (in timesteps)")
plt.ylabel(r'Linear fits for $\left\langle{r^2}\right\rangle$')
plt.legend()
plt.savefig("all_msd.png", dpi = 300, bbox_inches='tight')
plt.show()