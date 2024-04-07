import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
# Below taken from "Output structured data from LAMMPS" documentation
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader
#---------------------------------------------------------------------------------------
# the below block should technically be loopable over different simulation times
docs = ""
with open("log_nve_200ps.lammps") as f:
    for line in f:
        m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
        if m: docs += m.group(0) + '\n'
thermo = list(yaml.load_all(docs, Loader=Loader))
thermo_nve_200ps = pd.DataFrame(data=thermo[0]['data'], columns=thermo[0]['keywords'])

plt.figure(figsize=(12.8,4.8))
plt.title(r'Variation of velocity auto-correlation function with time')
plt.plot(thermo_nve_200ps['Step']/1000, thermo_nve_200ps['v_diff'])
plt.xlabel(r'Time (in ps)')
plt.ylabel(r'Instantaneous VACF (in $\AA^2 fs^{-2}$)')
# plt.savefig("A5_Q2_2c.png", dpi=300, bbox_inches='tight')
D = np.trapz(np.array(thermo_nve_200ps['v_diff']), np.array(thermo_nve_200ps['Step']))/3
print("Diffusion constant calculated from VACF is " + str(D))