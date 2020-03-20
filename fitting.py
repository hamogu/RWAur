import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from base_fit import *

for i, obsid in enumerate(['14539', '17644', '17764', '19980', '21176']):
    load_data(i + 1, obsid + '_A_grp.pi')
    load_bkg(i + 1, obsid + '_A_bkg.pi')

# For plotting, use merged data, for fitting use spearate
load_data(34, '2017_A_src.pi')
load_bkg(34, '2017_A_bkg.pi')

for i in range(1, 7):
    ungroup(i)

for i in range(1,7):
    ignore_bad(i)

ignore(None, 0.3)
ignore(9., None)

set_bkg_source(1, scale1d.scaleB * xsphabs.a1 * (xsvapec.v11 + xsvapec.v12))
set_bkg_source(2, scale1d.scaleB * xsphabs.a1 * (xsvapec.v21 + xsvapec.v22))
set_bkg_source(3, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))
set_bkg_source(4, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))
set_bkg_source(6, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))
set_bkg_source(5, scale1d.scaleB * xsphabs.a1 * (xsvapec.v41 + xsvapec.v42))

load_pars('RWAurB.pars', [a1, v11, v12, v21,v22, v31, v32])

for model in [a1, v11, v12, v21,v22, v31, v32, v41, v42]:
        for par in model.pars:
                par.frozen=True

fit_bkg()
# result of fit is
scaleB.c0 = 0.047
scaleB.c0.frozen = True

set_source(1, xsphabs.Aa1 * (xsvapec.Av11 + xsvapec.Av12))
set_source(2, xsphabs.Aa2 * (xsvapec.Av21 + xsvapec.Av22))
set_source(3, xsphabs.Aa3 * (xsvapec.Av31 + xsvapec.Av32))
set_source(4, Aa3 * (Av31 + Av32))
set_source(6, Aa3 * (Av31 + Av32))
set_source(5, xsphabs.Aa4 * (xsvapec.Av41 + xsvapec.Av42))

Av11.Ne.frozen = False
Av12.Ne = Av11.Ne
Av11.Fe.frozen = False
Av12.Fe = Av11.Fe
Av12.kT = 20
Av12.kT.frozen=True


Av21.Ne = Av11.Ne
Av22.Ne = Av21.Ne
Av21.Fe = Av11.Fe
Av22.Fe = Av21.Fe
Av21.kT = Av11.kT
Av22.kT = Av12.kT


Av31.Fe.frozen = False
Av32.Fe = Av31.Fe
Av32.kT = 20
Av32.kT.frozen = True
# Set values close to final to speed up convergence
Aa3.nH = 45
Av31.kT = 1
Av31.Fe = 50

set_stat('cash')
fit(1)
fit(2)
fit(3,4)
fit(5)
save_pars('RWAurA13_2T.pars', [Aa1, Av11, Av12], clobber=True)
save_pars('RWAurA15_2T.pars', [Aa2, Av21, Av22], clobber=True)
save_pars('RWAurA17_2T.pars', [Aa3, Av31, Av32], clobber=True)
save_pars('RWAurA18_2T.pars', [Aa4, Av41, Av42], clobber=True)

conf(1)
conf(2)
conf(3,4)
conf(5)
### Results of conf runs
Dataset               = 1
Confidence Method     = confidence
Iterative Fit Method  = None
Fitting Method        = levmar
Statistic             = cash
confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   Aa1.nH          0.0983409   -0.0591226    0.0652337
   Av11.kT          0.617837    -0.176419     0.102258
   Av11.Ne           1.88799     -1.02466      1.49671
   Av11.Fe          0.492003    -0.138411     0.216155
   Av11.norm     4.83776e-05 -1.55658e-05  1.78623e-05
   Av12.norm     4.12399e-05 -7.08837e-06  7.66724e-06

Dataset               = 2
Confidence Method     = confidence
Iterative Fit Method  = None
Fitting Method        = levmar
Statistic             = cash
confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   Aa2.nH            3.34694     -1.82285      12.0447
   Av21.norm     5.54996e-06        -----   0.00131743
   Av22.norm     2.06904e-05 -8.93076e-06  3.25969e-05

Datasets              = 3, 4
Confidence Method     = confidence
Iterative Fit Method  = None
Fitting Method        = levmar
Statistic             = cash
confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   Aa3.nH            36.6872     -9.88855      12.4498
   Av31.kT           1.36547     -0.27773     0.603206
   Av31.Fe            15.098     -8.24331      37.6198
   Av31.norm      0.00188157  -0.00129619   0.00368962
   Av32.norm     8.12265e-05 -7.72806e-05   7.3497e-05
sherpa-58>


# Group for plotting
for i in [1,2,5,6]:
    group_counts(i, 5)

for i in [1,2,5,6]:
    subtract(i)

plot_fit(1)
log_scale()
plot_fit(2, overplot=True)
plot_fit(5, overplot=True)
plot_fit(6, overplot=True)

colors = ['red', 'blue', 'green', 'default']
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))

# for i, idn in enumerate([1,2, 5]):
#     plot_bkg(idn, overplot=True)
#     plot_bkg_model(idn, overplot=True)
#     # maybe color that gray to it fades away more
#     set_curve('crv{0}'.format(7 + i), "*.color=gray")
#     set_histogram('hist{0}'.format(i + 1), "*.color=gray")

def make_plot_nice():
    add_label(1.5, 0.03 * .6**2, "2013-Jan-12", ["color", "red"])
    add_label(1.5, 0.03 * 0.6, "2015-Apr-16", ["color", "blue"])
    add_label(1.5, 0.03, "2017-Jan (merged)", ["color", "default"])
    set_label("all", ['size', 30])
    # no limits placed on background, but that's not an issue as long as we only use it for plotting.
    limits(X_AXIS, 0.4, 9.)
    limits(Y_AXIS, 5e-5, 0.05)
    # Now make the plot nicer
    set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
    set_axis("ax1","minortick.visible=0 tickformat=%3.1g label.size=30 ticklabel.size=26 offset.perpendicular=60")
    log_scale(X_AXIS)
    set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
    set_axis("ay1","label.size=30 offset.perpendicular=90.00 ticklabel.size=26 ")
    set_plot_title("")
    plot = get_plot()
    plot.rightmargin = 0.01
    plot.topmargin = 0.01
    plot.leftmargin = 0.17
    plot.bottommargin = 0.15
    set_plot(plot)

make_plot_nice()

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_subtracted.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_subtracted.pdf', ['export.clobber', True])


### Now get a 1T fit for 2017. Data sets 3,4 are still ungrouped and unsubtracted.
set_source(3, xsphabs.Aa3 * xsvapec.Av31)
set_source(4, Aa3 * Av31)

fit(3,4)
save_pars('RWAurA17_1T.pars', [Aa3, Av31], clobber=True)
conf(3,4)

Datasets              = 3, 4
Confidence Method     = confidence
Iterative Fit Method  = None
Fitting Method        = levmar
Statistic             = cash
confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   Aa3.nH            28.5093     -8.25681       12.021
   Av31.kT            3.1016     -1.35362      1.84141
   Av31.Fe           5.03496      -1.9538      3.42934
   Av31.norm     0.000721588 -0.000393311   0.00186176


### Get fluxes for L_X
set_source(3, xsphabs.Aa3 * (xsvapec.Av31 + xsvapec.Av32))
set_source(4, Aa3 * (Av31 + Av32))
load_pars('RWAurA17_2T.pars', [Aa3, Av31, Av32])
Aa1.nH = 0
Aa2.nH = 0
Aa3.nH = 0
calc_energy_flux(.3, 9., 1)
calc_energy_flux(.3, 9., 2)
calc_energy_flux(.3, 9., 3)

set_source(3, xsphabs.Aa3 * xsvapec.Av31)
set_source(4, Aa3 * Av31)
load_pars('RWAurA17_1T.pars', [Aa3, Av31])
Aa3.nH = 0
calc_energy_flux(.3, 9., 3)
