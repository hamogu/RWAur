import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from utils import save_conf
from shmodelshelper import load_pars, copy_pars

for i, obsid in enumerate(['14539', '17644', '17764', '19980']):
    load_data(i + 1, obsid + '_A_grp.pi')
    load_bkg(i + 1, obsid + '_A_bkg.pi')

# For plotting, use merged data, for fitting use spearate
load_data(5, '2017_A_src.pi')
load_bkg(5, '2017_A_bkg.pi')

for i in [1, 2, 3, 4, 5]:
    ignore_bad(i)

#ignore(None, 0.3)
#ignore(9., None)

for i in [1,2,3,4, 5]:
    group_counts(i, 5)

set_xsabund("angr")  # for consistency with Guedel et al 2014 and Schneider et al 2015
set_source(1, xsphabs.a1 * (xsvapec.v11 + xsvapec.v12))
set_source(2, xsphabs.a2 * (xsvapec.v21 + xsvapec.v22))
set_source(3, xsphabs.a3 * (xsvapec.v31 + xsvapec.v32))
set_source(4, a3 * (v31 + v32))
set_source(5, a3 * (v31 + v32))

# Set it now just to defined the right model instances in sherpa language
set_bkg_source(1, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
# Now overwrite with what we want
set_bkg_source(1, scale1d.scaleB * xsphabs.B1a1 * (xsvapec.B1v1 + xsvapec.B1v2 + xsvapec.B1v3))
load_pars('RWAurBChan1.pars', [a1, v1, v2, v3])
for oldcomp, newcomp in zip([a1, v1, v2, v3], [B1a1, B1v1, B1v2, B1v3]):
    copy_pars(oldcomp, newcomp)
    for par in newcomp.pars:
        par.frozen=True

set_bkg_source(2, scale1d.scaleB * xsphabs.B2a1 * (xsvapec.B2v1 + xsvapec.B2v2 + xsvapec.B2v3))

load_pars('RWAurBChan2.pars', [a1, v1, v2, v3])
for oldcomp, newcomp in zip([a1, v1, v2, v3], [B2a1, B2v1, B2v2, B2v3]):
    copy_pars(oldcomp, newcomp)
    for par in newcomp.pars:
        par.frozen=True

for i in [3,4, 5]:
    set_bkg_source(i, scale1d.scaleB * xsphabs.B3a1 * (xsvapec.B3v1 + xsvapec.B3v2 + xsvapec.B3v3))

load_pars('RWAurBChan3.pars', [a1, v1, v2, v3])
for oldcomp, newcomp in zip([a1, v1, v2, v3], [B3a1, B3v1, B3v2, B3v3]):
    copy_pars(oldcomp, newcomp)
    for par in newcomp.pars:
        par.frozen=True

fit_bkg()
# result of fit is
scaleB.c0 = 0.0475223
scaleB.c0.frozen = True

v11.Fe = 0.41
v11.Ne = 1.39

for v in [v12, v21, v22, v31, v32]:
    v.Fe = v11.Fe
    v.Ne = v11.Ne

v12.norm = 3.6 / 2.7 * v11.norm
v22.norm = 3.6 / 2.7 * v21.norm
v32.norm = 3.6 / 2.7 * v31.norm

for v in [v12, v22, v32]:
    v.kT = 20.
    v.kT.frozen = True

for v in [v21, v31]:
    v.kT = v11.kT


v11.kT = 0.63
v11.kT.frozen = True


fit(1,2,3,4)
set_conf_opt("sigma", 1.645)
conf(1,2,3,4)
# Saving the same confidence results three times, because save_conf
# cannot calculate more than one flux
# Easier to write a small file three times than to generalize save_conf
save_conf('spec_fit.json', energy_flux=1, absorbpars=[a1.nH])
save_conf('spec_fit2.json', energy_flux=2, absorbpars=[a2.nH])
save_conf('spec_fit34.json', energy_flux=3, absorbpars=[a3.nH])

for i in [1,2,3,4]:
    subtract(i)

plot_fit(1)
log_scale()
plot_fit(2, overplot=True)
plot_fit(5, overplot=True)


colors = ['red', 'blue', 'default']
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))

for i, idn in enumerate([1,2, 5]):
    plot_bkg(idn, overplot=True)
    plot_bkg_model(idn, overplot=True)
    # maybe color that gray to it fades away more
    set_curve('crv{0}'.format(7 + i), "*.color=gray")
    set_histogram('hist{0}'.format(i + 1), "*.color=gray")

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

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec.pdf', ['export.clobber', True])


## Now make the same plot background subtracted
load_data(11, '14539_A_grp.pi')
load_bkg(11, '14539_A_bkg.pi')
load_data(12, '17644_A_grp.pi')
load_bkg(12, '17644_A_bkg.pi')
load_data(13, '2017_A_src.pi')
load_bkg(13, '2017_A_bkg.pi')


for i in [11, 12, 13]:
    group_counts(i, 5)

for i in [11, 12, 13]:
    subtract(i)


set_source(11, a1 * (v11 + v12))
set_source(12, a2 * (v21 + v22))
set_source(13, a3 * (v31 + v32))

plot_fit(11)
log_scale()
plot_fit(12, overplot=True)
plot_fit(13, overplot=True)
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))

make_plot_nice()
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_subtracted.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_subtracted.pdf', ['export.clobber', True])



confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   a1.nH          0.00783098        -----    0.0413849
   v11.kT           0.722306    -0.116153    0.0964096
   v11.norm      2.67566e-05 -2.80498e-06  4.16942e-06
   a2.nH             2.57738     -2.06077       43.963
   v21.norm      1.16333e-05 -8.76439e-06  9.47167e-05
   a3.nH             18.1823     -5.58806      8.55735
   v31.norm      0.000225849 -8.23658e-05  0.000118894


load_data('2017_A_src.pi')
load_bkg('2017_A_bkg.pi')


   Aa1.nH         43.0623
   Av1.norm       0.00982589
sherpa-180> Av1.kT.val
            1.1155738699235624
sherpa-181> Av1.Fe.val
            6.7456352246601794

That model is consistenyl about 1 sigma too low for all bins in the range 1-4 keV. This cna easily be fixed by adding a cooler component, but because of the large nH, th properties of this component are almost arbitrary. (e.g. ridiculous norm)
