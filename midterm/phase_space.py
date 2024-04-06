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
#-----------------------------------------------------------------------------------------------------------------
n1 = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
n1atoms = [0, 2625, 5250, 7875, 10500, 13125]
i = 1
for n1frac in n1: # looping over number fraction of 1, which serves as a loop over all systems
    d = []
    name = "n1_{}.dump".format(n1atoms[i-1]) 
    d = dump(name)
    for t in range(len(d)):
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 12))
        plt.subplots_adjust(top=0.93)
        fig.suptitle("Phase space visualization of system " + str(i) + " for timestep " + str(d[t]['timestep']))
        c = ['r' if row[1] == 1 else 'b' for row in d[t]['data']] # this checks for the atom type; type 1 atoms are plotted as red dots, type 2 are blue
        ax1.scatter([row[5] for row in d[t]['data']], [row[2] for row in d[t]['data']], s = 0.2, c = c)
        ax1.set_title("Phase space for X-components")
        ax1.set(xlabel = "$p_x$ (in LJ units)", ylabel = "$r_x$ (in LJ units)")
        
        ax2.scatter([row[6] for row in d[t]['data']], [row[3] for row in d[t]['data']], s = 0.2, c = c)
        ax2.set_title("Phase space for Y-components")
        ax2.set(xlabel = "$p_y$ (in LJ units)", ylabel = "$r_y$ (in LJ units)")
        
        ax3.scatter([row[7] for row in d[t]['data']], [row[4] for row in d[t]['data']], s = 0.2, c = c)
        ax3.set_title("Phase space for Z-components")
        ax3.set(xlabel = "$p_z$ (in LJ units)", ylabel = "$r_z$ (in LJ units)")
        
        ax4.scatter(np.sqrt(np.array([row[5] for row in d[t]['data']])**2 + np.array([row[6] for row in d[t]['data']])**2 + 
                            np.array([row[7] for row in d[t]['data']])**2),
                    np.sqrt(np.array([row[2] for row in d[t]['data']])**2 + np.array([row[3] for row in d[t]['data']])**2 + 
                            np.array([row[4] for row in d[t]['data']])**2),
                    s = 0.2, c = c)
        ax4.set_title("Phase space for vector magnitudes")
        ax4.set(xlabel = r'|$\vec{p}$| (in LJ units)', ylabel = r'|$\vec{r}$| (in LJ units)')
        # fig.savefig("midterm_phase_space_n2frac"+str(1.0 - n1frac)+"_tstep_" + str(d[t]['timestep']) + ".png", dpi = 300, bbox_inches='tight')
        plt.show()
    i += 1
    
