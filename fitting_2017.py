import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from base_fit import *

load_data(1, '17764_A_preflare_grp.pi')
load_bkg(1, '17764_A_preflare_bkg.pi')
load_data(2, '17764_A_flare_grp.pi')
load_bkg(2, '17764_A_flare_bkg.pi')
load_data(3, '19980_A_grp.pi')
load_bkg(3, '19980_A_bkg.pi')

for i in [1,2,3]:
    ungroup(i)

for i in [1, 2, 3]:
    ignore_bad(i)

ignore(None, 0.3)
ignore(9., None)

# Need to define model comps v11 etc, or loading will not work
set_bkg_source(1, scale1d.scaleB * xsphabs.a1 * (xsvapec.v11 + xsvapec.v12))
set_bkg_source(2, scale1d.scaleB * xsphabs.a1 * (xsvapec.v21 + xsvapec.v22))
# Now define the models we really want
set_bkg_source(1, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))
set_bkg_source(2, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))
set_bkg_source(3, scale1d.scaleB * xsphabs.a1 * (xsvapec.v31 + xsvapec.v32))

load_pars('RWAurB.pars', [a1, v11, v12, v21,v22, v31, v32])

for model in [a1, v11, v12, v21,v22, v31, v32]:
        for par in model.pars:
                par.frozen=True

fit_bkg()
# result of fit is
scaleB.c0 = 0.047
scaleB.c0 = 0.0590558
scaleB.c0.frozen = True

set_source(1, xsphabs.Aa1 * (xsvapec.Av11 + xsvapec.Av12))
set_source(2, xsphabs.Aa2 * (xsvapec.Av21 + xsvapec.Av22))
set_source(3, xsphabs.Aa3 * (xsvapec.Av31 + xsvapec.Av32))


Av11.Fe.frozen = False
Av12.Fe = Av11.Fe
Av12.kT = 20
Av12.kT.frozen=True

Av21.Fe.frozen = False
Av22.Fe = Av21.Fe
Av22.kT = Av12.kT

Av31.Fe.frozen = False
Av32.Fe = Av31.Fe
Av32.kT = Av12.kT
# Set values close to final to speed up convergence
Aa3.nH = 45
Av31.kT = 1
Av31.Fe = 5

for model in [Av12, Av22, Av32]:
    model.norm = 0
    model.norm.frozen=True

set_stat('cash')
fit(1,2,3)
save_pars('RWAurA_2017_preflare_2T.pars', [Aa1, Av11, Av12], clobber=True)
save_pars('RWAurA_2017_flare_2T.pars', [Aa2, Av21, Av22], clobber=True)
save_pars('RWAurA_2017_obs2_2T.pars', [Aa3, Av31, Av32], clobber=True)

conf(1,2,3)




### Results of conf runs

Datasets              = 1, 2, 3
Confidence Method     = confidence
Iterative Fit Method  = None
Fitting Method        = levmar
Statistic             = cash
confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   Aa1.nH            36.7717     -12.3141      26.7759
   Av11.kT           2.26396     -1.31201      2.16127
   Av11.Fe           4.17469      -1.8481      1065.81
   Av11.norm      0.00148825  -0.00105477    0.0135662
   Aa2.nH            19.0353     -9.67332      26.4623
   Av21.kT           12.7255     -9.76201      7.94191
   Av21.Fe           454.255     -450.437       4237.6
   Av21.norm     2.83516e-05  -2.3949e-05   0.00184874
   Aa3.nH            21.3661     -15.2155      16.8008
   Av31.kT            1.6327     -0.60596      17.5088
   Av31.Fe            10.009     -7.97029      4376.34
   Av31.norm      0.00073919 -0.000734417   0.00397091

# Group for plotting
for i in [1,2,3]:
    group_counts(i, 5)

for i in [1,2,3]:
    subtract(i)

plot_fit(1)
log_scale()
plot_fit(2, overplot=True)
plot_fit(3, overplot=True)


colors = ['red', 'blue', 'default']
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))

add_label(1.5, 0.01 * .6**2, "obs 1: preflare", ["color", "red"])
add_label(1.5, 0.01 * 0.6, "obs 1: flare", ["color", "blue"])
add_label(1.5, 0.01, "obs 2", ["color", "default"])
set_label("all", ['size', 30])
# no limits placed on background, but that's not an issue as long as we only use it for plotting.
limits(X_AXIS, 1, 9.)
limits(Y_AXIS, 5e-6, 0.02)
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


print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_2017_flare.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_2017_flare.pdf', ['export.clobber', True])


### Get fluxes for L_X
Aa1.nH = 0
Aa2.nH = 0
Aa3.nH = 0
calc_energy_flux(.3, 9., 1)
calc_energy_flux(.3, 9., 2)
calc_energy_flux(.3, 9., 3)
