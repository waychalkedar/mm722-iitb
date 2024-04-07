# Attempting what I saw on https://youtu.be/Wvdk8a_nRJg
import numpy as np
import matplotlib.pyplot as plt
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader
from scipy.integrate import quad
from scipy.optimize import fsolve, root
from scipy.interpolate import make_interp_spline, BSpline

tstep = [0, 3, 6, 9, 11]
cutoff = [2, 2.5, 3, 3.5, 4, 4.5, 5]

for cut in cutoff:
    plt.figure(figsize=(9.6, 4.8))
    docs = ""
    tmp = []
    with open("tmp_" + str(cut) + ".yaml", "r") as f:
        for line in f:
            m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
            if m: docs += m.group(0) + '\n'
    tmp = np.array(list(yaml.load_all(docs, Loader=Loader)))
    rdf = [{'timestep': 0, 'data': []}] * 12
    rdf[11]['timestep'] = 11*10000
    rdf[11]['data'] = tmp[0]['data'][(100*11):(100*11+100)]
    rdfval = []
    r= []
    for k in range(100):
        r.append((rdf[11]['data'][k][0]))
        rdfval.append(rdf[11]['data'][k][1])
    cross = 0
    x = []
    y = []
    rnew = np.linspace(np.array(r).min(), np.array(r).max(), 1500)
    rdfnew = make_interp_spline(r, rdfval, k=3)
    funcnew = rdfnew(rnew)
    for i in range(len(rnew)-1): # this finds the timestep at which the RDF vs t curve crosses RDF = 1    
        if np.logical_and(rdfnew(rnew[i]) < 1.0, rdfnew(rnew[i+1])  > 1.0):
            cross+=1
        if cross == 1:
            x.append(rnew[i])
            y.append(rdfnew(rnew[i])*rnew[i]*rnew[i])
            # y.append(rdfnew(rnew[i]))
        if np.logical_and(rdfnew(rnew[i]) > 1.0, rdfnew(rnew[i+1]) < 1.0):
            cross+=1
    
    xnew = np.linspace(np.array(x).min(), np.array(x).max(), 1500)
    ypnew = make_interp_spline(rnew, funcnew, k=3)
    ynew = ypnew(xnew)
    
    plt.scatter(r, rdfval, label = "Area is " + str(np.trapz(np.multiply(ynew, xnew**2), xnew)*4*np.pi))
    # plt.scatter(xnew, ynew, label = "Area is " + str(np.trapz(np.multiply(ynew, xnew**2), xnew, 0.01)*8*np.pi))
    plt.plot(rnew, funcnew, 'r', linewidth = 1.0)
    plt.plot(np.linspace(0, 5, 100), [1.0]*100, 'k--') 
    plt.fill_between(x, rdfnew(x), alpha = 0.2, color = 'g',label = "First Shell")
    plt.title("Evaluation of average no. of neighbours with LJ cutoff = " + str(cut) + " at the 110000th timestep")
    plt.xlabel(r'Radial distance $r$')
    plt.ylabel("$r^2g(r)$")
    plt.xlim(0, 5.0)
    plt.legend()
    # plt.savefig("A6_calc_cut=" + str(cut) + "_tstep=" + str(i*10000) + ".png", dpi = 300, bbox_inches = 'tight')
    plt.show()    
