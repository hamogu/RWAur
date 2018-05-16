'''Fit Fe 6.62 / 6.7 keV line in XMM and Chandra with a Gauss.

Load Models for XMM and Chandra 2017 (which are fit in other scripts)
make plot for paper.
'''
import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from base_fit import *

from utils import save_conf
from shmodelshelper import save_pars, load_pars

#### XMM ####
load_data(11, xmmpath + 'spec_fullflare_EPN.15grp')
load_data(12, xmmpath + 'spec_fullflare_EMOS1.15grp')
load_data(13, xmmpath + 'spec_fullflare_EMOS2.15grp')

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
fit(11, 12, 13)
conf(11, 12, 13)
save_pars('FelineXMM.pars', [c1, g1], clobber=True)

#### Chandra 2017 ####
for i, obsid in enumerate(['17764', '19980']):
    load_data(i + 1, obsid + '_A_grp.pi')
    load_bkg(i + 1, obsid + '_A_bkg.pi')

# For plotting, use merged data, for fitting use spearate
load_data(3, '2017_A_src.pi')
load_bkg(3, '2017_A_bkg.pi')

for i in [1, 2, 3]:
    ignore_bad(i)

ignore(None, 5.)
ignore(7.5, None)
notice(5., 7.5)
group_counts(1, 1)
group_counts(2, 1)
group_counts(3, 5)

for i in [1,2,3]:
    # Fit the Fe line
    set_source(i, const1d.c1 + gauss1d.g1)

# Set reasonable starting values to ensure convergence
c1.c0 = 0
g1.pos = 6.6
g1.fwhm = 0.2
g1.ampl = 1e-5
fit(1,2)
conf(1,2)
save_pars('FelineChandra.pars', [c1, g1], clobber=True)


#### Now on to the plot ####

set_model(3, xsphabs.Aa3 * (xsvapec.Av31 + xsvapec.Av32))
load_pars('RWAurA17_2T.pars', [Aa3, Av31, Av32])

notice(3., 8.)
plot_fit(3)
set_curve('crv2', "*.color=default")

limits(X_AXIS, 3, 8.)
limits(Y_AXIS, 3e-5, 0.011)
# Now make the plot nicer

set_axis("ax1","minortick.visible=1 tickformat=%3.1g label.size=30 ticklabel.size=26 offset.perpendicular=65")
set_arbitrary_tick_positions("ax1",[3,4,5,6,7,8],["3","4","5","6","7","8"])
set_axis("ay1","label.size=30 offset.perpendicular=80.00 ticklabel.size=26")
set_plot_title("")

plot = get_plot()
plot.rightmargin = 0.02
plot.topmargin = 0.01
plot.bottommargin = 0.15
set_plot(plot)

# Now make the inset
add_plot(0.25,0.45,0.65,0.92)
plot_fit(3, overplot=True)
set_curve('crv2', "*.color=default")
limits(X_AXIS, 6.2, 7.2)
set_axis("ax1","minortick.visible=1 tickformat=%3.2g ticklabel.size=20")
set_axis("ay1","ticklabel.size=20")
#v1.kT = 5.5
#v1.kT.frozen = True
#fit(1, 2)
#plot_fit(3, overplot=True)
#set_curve('crv4', "*.color=default line.style=longdash")


# Now back to the inset and add XMM there.
# Note that the XMM parameter file re-uses the name "v1" and thus
# overwrites the value of the Chandra v1 defined above.
current_plot("plot2")

set_model(11, xsphabs.a1 * (xsvapec.v21 + xsvapec.v22))
load_pars('RWAurXMMflare.pars', [a1, v21, v22])
for v in [v21, v22]:
    for p in v.pars:
        p.link = None

# roughly rescale XMM data by ratio of arfs at 6.7 keV
set_exposure(11, get_exposure(11) / 95.*660.)
# In the model, some components are linked to model components that
# we did not load here, so it uses some default.
# The numerical value is in the files too, we just have to unlink.

for v in [v21, v22]:
    v.norm = v.norm.val * 95./660.

plot_fit(11, overplot=True)
set_curve('crv3', "*.color=olive")
set_curve('crv3', "symbol.fill=True")
set_curve('crv4', "*.color=olive")
limits(X_AXIS, 6.2, 7.2)
limits(Y_AXIS, 3e-5, 0.02)

add_vline(6.63, "color=skyblue line.thickness=4 depth=1")
add_vline(6.7, "color=skyblue line.thickness=4 depth=1")

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_17.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_17.pdf', ['export.clobber', True])


### Answer referee's question on how important the binning is
ignore(None, 5.)
ignore(7.5, None)

for n in [1,2,3,4,5,6,7,10]:
    notice(5., 7.5)
    group_counts(1, n)
    group_counts(2, n)
    # Set reasonable starting values to ensure convergence
    c1.c0 = 0
    g1.pos = 6.6
    g1.fwhm = 0.2
    g1.ampl = 1e-5
    print '##### n = {} #####'.format(n)
    fit(1,2)
    conf(1,2)

print '##### cash #####'.format(n)
set_stat("cash")
ungroup(1)
ungroup(2)
ignore(None, 5.)
ignore(7.5, None)

fit(1,2)
conf(1,2)

# Here is a table of results:
# Chi^2 statistic with Gehrels weighting in Sherpa
# (all numbers are 90% confidence intervals)
# n=1: 6.62 +- 0.04
# n=2: 6.62 -0.03 +0.04
# n=3: 6.62 +- 0.03
# n=4: 6.63 +- 0.04
# n=5: 6.62 +- 0.03
# n=6: 6.63 +- 0.04
# n=7: 6.62 +- 0.03
# n=10: 6.64 -0.08 + 0.04 -- in this regime there are only 4 bins over the range of the feature and thus the fit is not as good any longer

# Cash statistic: 6.63 +- 0.02
