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

ignore(None, .2)
for i in range(5):
    for j in [1,2,3]:
        ignore_bad(i * 10 + j)

ignore(None, .2)
ignore(8., None)

for i in range(1, 6):
    group_counts(i, 30)

ignore(None, .2)

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








load_data(11, xmmpath + 'RWAur_1319_0401870301_EPN_S003_spec.15grp')
load_data(12, xmmpath + 'RWAur_1319_0401870301_EMOS1_S001_spec.15grp')
load_data(13, xmmpath + 'RWAur_1319_0401870301_EMOS2_S002_spec.15grp')

for i in [11,12,13]:
    # Fit the Fe line
    set_source(i, const1d.c1 + gauss1d.g1)

ignore(7.5, None)
ignore(None, 6.)

group_counts(11, 25)
# Set reasonable starting values to ensure convergence
g1.pos = 6.7
g1.fwhm = 0.2
g1.ampl = 1e-5
fit(11)
conf(11)
save_pars('Feline.pars', [c1, g1], clobber=True)

# So, we have a super normal 6.7 keV line.

#subtract(11)
for i in [11,12,13]:
    group_counts(i, 25)

notice(None, None)
ignore(None, .2)
ignore(9., None)

for i in [11,12,13]:
    # Global fit
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
fit(11, 12, 13)
save_pars('RWAurXMM.pars', [a1, v1, v2, v3], clobber=True)
conf(11, 12, 13)

save_conf('fit_XMM.json', energy_flux=11, absorbpars=[a1.nH])

# The Chandra data has much fewer counts.
# We just want to know here is the spectra are compatible
# in general, so we fix many of the parameters.
v1.Fe.frozen = True
v1.Ne.frozen = True
v1.kT.frozen = True
v2.kT.frozen = True
v3.kT.frozen = True

### Fitting Chandra data from B
for i, obsid in enumerate(['14539', '17644', '17764', '19980']):
    load_data(i + 1, obsid + '_B_grp.pi')
    load_bkg(i + 1, obsid + '_B_bkg.pi')

for i in [1, 2, 3, 4]:
    ignore_bad(i)


ignore(None, 0.3)
ignore(9., None)

for i in [1,2,3,4]:
    group_counts(i, 15)


for i in [1,2,3,4]:
    set_source(i, a1 * (v1 + v2 + v3))

for i in [3,4]:
    set_pileup_model(i, jdpileup.jdp)

fit(1)
save_pars('RWAurBChan1.pars', [a1, v1, v2, v3], clobber=True)
conf(1)
save_conf('chanB1.json', energy_flux=1, absorbpars=[a1.nH])


fit(2)
save_pars('RWAurBChan2.pars', [a1, v1, v2, v3], clobber=True)
conf(2)
save_conf('chanB2.json', energy_flux=2, absorbpars=[a1.nH])

fit(3,4)
save_pars('RWAurBChan3.pars', [a1, v1, v2, v3], clobber=True)
conf(3,4, a1.nH, v1.norm, v2.norm, v3.norm)
save_conf('chanB3.json', energy_flux=3, absorbpars=[a1.nH])
