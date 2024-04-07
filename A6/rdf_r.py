import numpy as np
import matplotlib.pyplot as plt
import re, yaml
try:
    from yaml import CSafeLoader as Loader
except ImportError:
    from yaml import SafeLoader as Loader

tstep = [0, 3, 6, 9, 11]
cutoff = [2, 2.5, 3, 3.5, 4, 4.5, 5]

#Storing slices of tmp into a separate list of dictionaries for easy handling
for k in range(len(tstep)):
    for cut in cutoff:
        docs = ""
        tmp = []
        with open("tmp_" + str(cut) + ".yaml", "r") as f:
            for line in f:
                m = re.search(r"^(keywords:.*$|data:$|---$|\.\.\.$|  - \[.*\]$)", line)
                if m: docs += m.group(0) + '\n'
        tmp = np.array(list(yaml.load_all(docs, Loader=Loader)))
        rdf = [{'timestep': 0, 'data': []}] * 12
        for i in range(tstep[k]+1):
            rdf[i]['timestep'] = i*10000
            rdf[i]['data'] = tmp[0]['data'][(100*i):(100*i+100)]
            r = []
            rdfval = []
        for g in range(100):
            r.append((rdf[i]['data'][g][0]))
            rdfval.append(rdf[i]['data'][g][1])
        if i == 11:
            plt.figure(figsize=(9.6, 4.8))
            plt.plot(r, rdfval, label = str(cut), linewidth=1.0)
            plt.title("Radial distribution function of system with LJ cutoff = " + str(cut) + " at the " + str(i*10000) + "th timestep")
            plt.xlabel(r'Radial distance')
            plt.ylabel("RDF")
            plt.xlim(0, 5.0)
            plt.legend()
            # plt.savefig("A6_cut=" + str(cut) + "_tstep=" + str(i*10000) + ".png", dpi = 300, bbox_inches = 'tight')
            plt.show()