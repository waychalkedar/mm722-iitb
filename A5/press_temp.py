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
    for s in ["nve", "nvt"]:
        docs = ""
        thermo = []
        with open("thermo_{}_{}.file".format(s, prod), "r") as f:
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
        fig, (axt, axp) = plt.subplots(1, 2, figsize=(12.8, 4.8))
        axt.plot(np.array(time)/1000, temp, 'r', linewidth=1.0)
        axt.set(xlabel="Time (in ps)", ylabel="Temperature (in K)")
        axp.plot(np.array(time)/1000, press, 'b', linewidth=1.0)
        axp.set(xlabel="Time (in ps)", ylabel="Pressure (in atmos)")
        if s == "nve":
            axt.set_title("Variation in temperature with time for a " + str(prod/1000) + " ps \n production run using an unrestrained NVE ensemble")
            axp.set_title("Variation in pressure with time for a " + str(prod/1000) + " ps \n production run using an unrestrained NVE ensemble")
        else:
            axt.set_title("Variation in temperature with time for a " + str(prod/1000) + " ps \n production run using an NVT ensemble")
            axp.set_title("Variation in pressure with time for a " + str(prod/1000) + " ps \n production run using an NVT ensemble")
        # fig.savefig("Q4_" + str(s) + "_TP_"+str(prod/1000)+".png", dpi=300, bbox_inches='tight')
    