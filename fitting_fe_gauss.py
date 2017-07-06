import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from utils import save_conf
from shmodelshelper import save_pars, load_pars

xmmpath = '/melkor/d1/guenther/downdata/XMM/RWAur/0401870301/'

set_conf_opt("sigma", 1.645)
set_conf_opt('numcores', 24)  # for melkor

for i, obsid in enumerate(['17764', '19980']):
    load_data(i + 1, obsid + '_A_grp.pi')
    load_bkg(i + 1, obsid + '_A_bkg.pi')

# For plotting, use merged data, for fitting use spearate
load_data(3, '2017_A_src.pi')
load_bkg(3, '2017_A_bkg.pi')


load_data(11, xmmpath + 'RWAur_1319_0401870301_EPN_S003_spec.15grp')
load_data(12, xmmpath + 'RWAur_1319_0401870301_EMOS1_S001_spec.15grp')
load_data(13, xmmpath + 'RWAur_1319_0401870301_EMOS2_S002_spec.15grp')


#for i in [1, 2, 3]:
#    ignore_bad(i)

ignore(None, 6.)
ignore(7.5, None)

group_counts(1, 5)
group_counts(2, 5)
group_counts(3, 5)
group_counts(11, 15)

for i in [1,2,3, 11,12,13]:
    # Fit the Fe line
    set_source(i, const1d.c1 + gauss1d.g1)

# Set reasonable starting values to ensure convergence
g1.pos = 6.6
g1.fwhm = 0.2
g1.ampl = 1e-5
fit(1,2)
conf(1,2)


# Set reasonable starting values to ensure convergence
g1.pos = 6.7
g1.fwhm = 0.2
g1.ampl = 1e-5
fit(11)
conf(11)
save_pars('Feline.pars', [c1, g1], clobber=True)


# Maybe just plot combined data with some models over it as an inset to the big figure
sherpa-50> ignore(None, 6.)
sherpa-51> ignore(7.5, None)
sherpa-52> plot_fit(3)
