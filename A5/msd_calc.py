import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# Below taken from "Output structured data from LAMMPS" documentation
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader
#-------------------------------------------------------------------------------
mass = {1: 1.008, 2: 15.9994}

def func(x, m):
    return m * x 
a = 4.5
b = 0.5
c = 50

for prod in [200000, 500000, 1000000]:
    prodtimesteps = [] 
    with open("solvate_" + str(prod) + ".dump", "r") as f:
            prodtimesteps = np.array(list(yaml.load_all(f, Loader=Loader)))
        
    # define com as a 2d matrix. First index of time, then a list of x, y, z
    com = np.zeros((len(prodtimesteps),3))
    n = 0
    msdt = []
    runavg = np.zeros((len(prodtimesteps),3))
    time = []
    for i in range(len(prodtimesteps)):
        for k in range(348):
            com[i][0] += mass[prodtimesteps[i]['data'][k][2]]*prodtimesteps[i]['data'][k][3] 
            com[i][1] += mass[prodtimesteps[i]['data'][k][2]]*prodtimesteps[i]['data'][k][4]
            com[i][2] += mass[prodtimesteps[i]['data'][k][2]]*prodtimesteps[i]['data'][k][5]
        com[i] = com[i]/(116*(2*mass[1]+mass[2]))
        msd_peratom = []
        for k in range(0, 348, 3):
            x_temp = prodtimesteps[i]['data'][k][3] - com[i][0] - runavg[i][0]
            y_temp = prodtimesteps[i]['data'][k][4] - com[i][1] - runavg[i][1]
            z_temp = prodtimesteps[i]['data'][k][5] - com[i][2] - runavg[i][2]
            runavg[i][0] = (runavg[i][0] * n + x_temp)/(n + 1)
            runavg[i][1] = (runavg[i][1] * n + y_temp)/(n + 1)
            runavg[i][2] = (runavg[i][2] * n + z_temp)/(n + 1)
            x_ref = prodtimesteps[0]['data'][k][3] - com[0][0]
            y_ref = prodtimesteps[0]['data'][k][4] - com[0][1]
            z_ref = prodtimesteps[0]['data'][k][5] - com[0][2]
            msd_peratom.append((x_temp - x_ref)**2 + (y_temp - y_ref)**2 + (z_temp - z_ref)**2)
        n += 1
        msdt.append(np.mean(msd_peratom))
        time.append(prodtimesteps[i]['timestep'])
    
    xdata = np.array(time)/1000
    ydata = msdt
    popt, pcov = curve_fit(func, xdata, ydata)
    plt.figure(figsize=(12.8, 4.8))
    plt.title("Calculated MSD vs time for a " + str(prod/1000) + " ps \n production run using an NVT ensemble")
    plt.scatter(xdata, ydata, s=0.2, label = "MSD calculated from .dump file")
    plt.plot(xdata, func(xdata, *popt), 'r', label = "y = " + str(f'{popt[0]:.4f}') + "x")
    plt.xlabel("Time (in ps)")
    plt.ylabel(r'$\left\langle{r^2}\right\rangle$')
    plt.legend(loc='lower right', markerscale=10)
    # plt.savefig("Q4_nvt_calc_msd_"+str(prod/1000)+".png", dpi=300, bbox_inches='tight')
