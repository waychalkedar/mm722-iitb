import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Below taken from "Output structured data from LAMMPS" documentation
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader

def read_data_from_file(filename):
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
#-------------------------------------------------------------------------------------------------
# the below block should technically be loopable over different simulation times
# the plan is to generate plots within the loop itself
for prod in [200000, 500000, 1000000]:
    docs = ""
    thermo = []
    with open("thermo_nve_" + str(prod) + ".file", "r") as f:
        for line in f:
            m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
            if m: docs += m.group(0) + '\n'
    thermo = np.array(list(yaml.load_all(docs, Loader=Loader)))
    time = []
    temp = []
    toteng = []
    press = []
    vacf = []
    D = 0.0
    for i in range(len(thermo[0]['data'])):
        time.append(thermo[0]['data'][i][0])
        temp.append(thermo[0]['data'][i][1])
        toteng.append(thermo[0]['data'][i][4])
        press.append(thermo[0]['data'][i][5])
        vacf.append(thermo[0]['data'][i][6])
    # plt.figure(figsize=(12.8, 4.8))
    # plt.title("Variation in temperature with time for a " + str(prod/1000) + " ps production run using an NVT ensemble")
    # plt.plot(np.array(time)/1000, temp, 'r', linewidth=1.0)
    # plt.xlabel("Time (in ps)")
    # plt.ylabel("Temperature (in K)")
    # plt.savefig("Q3_nvt_temp_" + str(prod/1000)+".png", dpi=300, bbox_inches='tight')
    # plt.show()
    # plt.figure(figsize=(12.8, 4.8))
    # plt.title("Variation in total energy with time for a " + str(prod/1000) + " ps production run using an NVT ensemble")
    # plt.plot(np.array(time)/1000, toteng, 'g', linewidth=1.0)
    # plt.xlabel("Time (in ps)")
    # plt.ylabel("Total energy (in kcal/mol)")
    # plt.savefig("Q3_nvt_toteng_" + str(prod/1000)+".png", dpi=300, bbox_inches='tight')
    # plt.show()
    # plt.figure(figsize=(12.8, 4.8))
    # plt.title("Variation in pressure with time for a " + str(prod/1000) + " ps production run using an NVT ensemble")
    # plt.plot(np.array(time)/1000, press, 'b', linewidth=1.0)
    # plt.xlabel("Time (in ps)")
    # plt.ylabel("Pressure (in atmos)")
    # plt.savefig("Q3_nvt_press_" + str(prod/1000)+".png", dpi=300, bbox_inches='tight')
    # plt.show()
    # plt.figure(figsize=(12.8, 4.8))
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.8, 4.8))
    ax2.set_title("VACF vs time for a " + str(prod/1000) + " ps production run \n using an unrestrained NVE ensemble")
    D = np.trapz(vacf, time)/3
    ax2.plot(np.array(time)/1000, vacf, 'm', linewidth=1.0, label = "Diffusion constant D =" + str(D) + " (in $\AA^2 fs^{-1}$)")
    ax2.set(xlabel="Time (in ps)", ylabel="Instantaneous VACF (in $\AA^2 fs^{-2}$)")
    ax2.legend()
    # Processing the dump file seems to be a very computationally heavy task. It will then be done separately
    # prodt = [] 
    # with open("solvate_nve_" + str(prod) + ".dump", "r") as f:
    #     # Data = yaml.load_all(f, Loader=Loader)
    #     # for d in Data:
    #     #     prodt.append(d)
    #     prodt = np.array(list(yaml.load_all(f, Loader=Loader)))
    
    msdt = read_data_from_file("msd_nve_" + str(prod) + ".txt")
    time = []
    msd = []
    for i in range(len(msdt)):
        time.append(msdt[i][0])
        msd.append(msdt[i][1])
    from scipy.optimize import curve_fit
    def func(x, m):
        return m * x 
    a = 4.5
    b = 0.5
    c = 50
    xdata = np.array(time)/1000
    ydata = msd
    popt, pcov = curve_fit(func, xdata, ydata)
    ax1.set_title("MSD vs time for a " + str(prod/1000) + " ps production run \n using an unrestrained NVE ensemble", wrap=True)
    ax1.scatter(xdata, ydata, s=0.2, label = "MSD data from LAMMPS")
    ax1.plot(xdata, func(xdata, *popt), 'r', label = "y = " + str(f'{popt[0]:.4f}') + "x")
    ax1.set(xlabel="Time (in ps)", ylabel=r'$\left\langle{r^2}\right\rangle$')
    ax1.legend(loc='lower right', markerscale=10)
    # fig.savefig("Q3_nve_D_"+str(prod/1000)+".png", dpi=300, bbox_inches='tight')
