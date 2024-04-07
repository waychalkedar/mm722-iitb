import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#----------------------------------------------------------------------------------
# From ChatGPT
def extract_columns_from_multiple_csv(csv_files):
    all_columns = {}
    for csv_file in csv_files:
        # Read the CSV file using pandas
        df = pd.read_csv(csv_file, delim_whitespace=True)
        # Extract each column into separate lists
        columns = [df[column].tolist() for column in df.columns]
        # Store extracted columns in the dictionary with file name as key
        file_name = csv_file.split('/')[-1]  # Extract file name from path
        all_columns[file_name] = columns
    return all_columns

# Example usage
csv_files = ['msd_200ps.txt'] 
msd200ps = extract_columns_from_multiple_csv(csv_files) # a dictionary

from scipy.optimize import curve_fit

def func(x, m):
    return m * x 
# Fit the function a * np.exp(b * t) + c to x and y
a = 4.5
b = 0.5
c = 50
xdata = np.array(msd200ps['msd_200ps.txt'][0])/1000
ydata = np.array(msd200ps['msd_200ps.txt'][1])
popt, pcov = curve_fit(func, xdata, ydata)
# print(popt)

# Example syntax below
# plt.plot(xdata, func(xdata, *popt), 'r', label = r'y = $-0.7985e^{-0.3879x}$ + 0.1526')

# Below is the plot for method 1 - using msd file
plt.figure(figsize=[12.8, 4.8])
plt.scatter(xdata, ydata, s=0.2, label='Data from msd.txt LAMMPS output')
plt.plot(xdata, func(xdata, *popt), 'r', label="y = " + str(f'{popt[0]:.4f}') + r'x')
plt.title(r'Mean square displacement versus time for 200 ps production')
plt.xlabel(r'Time (in ps)')
plt.ylabel(r'$\left\langle{r^2}\right\rangle$')
plt.legend(loc='lower right', markerscale=10)
# plt.savefig("A5_Q2_1.png", dpi=300, bbox_inches='tight')
plt.show()
