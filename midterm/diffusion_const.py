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
# ----------------------------------------------------------------------------------------------------------------------------
i = 0
d = np.zeros(6)
for n1 in [0, 2625, 5250, 7875, 10500, 13125]: # looping over all systems
    msd1 = read_data("msd_atom1_n1={}.txt".format(n1)) 
    msd2 = read_data("msd_atom2_n1={}.txt".format(n1))
    x = [int(row[0]) for row in msd1]
    y1 = [row[1] for row in msd1]
    y2 = [row[1] for row in msd2]
    popt1, pcov1 = curve_fit(line, x, y1)
    popt2, pcov2 = curve_fit(line, x, y2)
    if n1 == 0:
        fig, (ax1, ax2) = plt.subplots(2, figsize=(9.6, 10))
        for ax in [ax1, ax2]:
            ax.scatter(x, y2, s=0.4, label = 'MSD data from LAMMPS')
            ax.plot(x, line(np.array(x), *popt2), 'r', label = r'$y = $' + str(f'{popt2[0]:.4f}') + r'$x$')
            ax.set_title("Calculation of diffusion constant for type 2 atoms in system 1 with $n_2=1.0$")
            ax.set(xlabel = "Time (in timesteps)", ylabel = r'$\left\langle{r^2}\right\rangle$')
            ax.legend(markerscale=4.0)
            if ax == ax2:
                ax.set_xlim(400000, 600000)
                ax.set_ylim(200,600)
        # fig.savefig("msd_n1=" + str(n1), dpi = 300, bbox_inches='tight')
        plt.show()
        d[i] = 100*popt2[0]/6
        i += 1
        continue
    fig, (ax1, ax2) = plt.subplots(2, figsize=(9.6, 10))
    for ax in [ax1, ax2]:
        ax.scatter(x, y1, s=0.4, label = 'MSD data from LAMMPS')
        ax.plot(x, line(np.array(x), *popt1), 'r', label = r'$y = $' + str(f'{popt1[0]:.4f}') + r'$x$')
        ax.set_title("Calculation of diffusion constant for type 1 atoms in system " + str(i+1) + " with $n_2=$" + str(1-(n1/13125)))
        ax.set(xlabel = "Time (in timesteps)", ylabel = r'$\left\langle{r^2}\right\rangle$')
        ax.legend(markerscale=4.0)
        if ax == ax2:
            ax.set_xlim(400000, 600000)
            ax.set_ylim(200,600)
    # fig.savefig("msd_n1=" + str(n1), dpi = 300, bbox_inches='tight')
    plt.show()
    d[i] = 100*popt1[0]/6
    i += 1

n2frac = [1.0, 0.8, 0.6, 0.4, 0.2, 0.0]
col = ['b' if n == 1.0 else 'r' for n in n2frac]
plt.scatter(n2frac, d, c = col)
texts = [plt.text(n2frac[i], d[i], str(f'{d[i]:.4f}')) for i in range(len(n2frac))]
adjust_text(texts, x=n2frac, y=d, arrowprops=dict(arrowstyle="-", color='r', lw=0.5))
plt.title("Variation in diffusion constant with number fraction of 2")
plt.xlabel("$n_2$")
plt.ylabel("$D$ (in LJ units of length$^2$/time)")
# plt.savefig("diff_vs_n.png", dpi = 300, bbox_inches='tight')
plt.show()