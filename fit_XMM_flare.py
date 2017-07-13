import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from utils import save_conf
from shmodelshelper import save_pars, load_pars

xmmpath = '/melkor/d1/guenther/downdata/XMM/RWAur/0401870301/'

set_conf_opt("sigma", 1.645)
set_conf_opt('numcores', 24)  # for melkor

set_xsabund("angr")  # for consistency with Guedel et al 2014 and Schneider et al 2015


tintervals = ['quiet', 'rise', 'top', 'decay1', 'decay2']
colors = ['black', 'red', 'olive', 'blue', 'magenta']
for i, name in enumerate(tintervals):
    load_data(i * 10 + 1, xmmpath + "spec_{}_EPN.15grp".format(name))
    load_data(i * 10 + 2, xmmpath + "spec_{}_EMOS1.15grp".format(name))
    load_data(i * 10 + 3, xmmpath + "spec_{}_EMOS2.15grp".format(name))

for i in range(1, 6):
    group_counts(i, 30)

ignore(None, .2)
ignore(9., None)

for i in range(1, 6):
    plot_data(i, overplot=(i > 1))
    if i > 1:
        set_curve('crv{:d}'.format(i), "*.color=" + colors[i-1])

for i in range(1,6):
    set_model(i, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))



for v in [v2, v3]:
    for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
        setattr(v, elem, getattr(v1, elem))


v1.Fe.frozen = False
v1.Si = v1.Fe
v1.Mg = v1.Fe
v1.Ne.frozen = False

# Set to reasonable values before fit to speed convergence
a1.nH = 0.2
v1.kT = 0.3
v2.kT = 1.5
v3.kT = 5.

v1.kT.frozen = True
v2.kT.frozen = True
v3.kT.frozen = True
a1.nH.frozen = True
v1.Ne = 2.3
v1.Ne.frozen = False
v1.Fe = 0.6
v1.Fe.frozen = False

for i in range(5):
    set_model(i * 10 + 1, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
    set_model(i * 10 + 2, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
    set_model(i * 10 + 3, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
    fit(i * 10 + 1, i*10+2,i*10+3)
