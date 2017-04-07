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
for i in [1,2,3,4, 5]:
    set_bkg_source(i, xsphabs.Ba1 * (xsvapec.Bv2 + xsvapec.Bv1))

# Set RW Aur B to the values found in Skinner and Guedel
Ba1.nH = 0.043
Ba1.nH.frozen = True
Bv1.kT = 0.98
Bv1.kT.frozen = True
Bv2.kT = 3.15
Bv2.kT.frozen = True
Bv1.Ne = 1.69
Bv1.Fe = 0.36
Bv2.Ne = Bv1.Ne
Bv2.Fe = Bv1.Fe
fit_bkg()
# result of fit is
Bv2.norm = 8.08734e-06
Bv1.norm = 4.85221e-06
Bv1.norm.frozen = True
Bv2.norm.frozen = True

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
    v.kT.frozen=True

for v in [v21, v31]:
    v.kT = v11.kT


v11.kT = 0.63
v11.kT.frozen = True


fit(1,2,3,4)
set_conf_opt("sigma", 1.645)
conf(1,2,3,4)
confres = get_conf_results()
import json
with open('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_fit.json', 'w') as f:
    json.dump({'name': confres.parnames, 'val': confres.parvals,
               'up': confres.parmaxes, 'down': confres.parmins}, f)

for i in [1,2,3,4]:
    subtract(i)

plot_fit(1)
log_scale()
plot_fit(2, overplot=True)
plot_fit(5, overplot=True)


colors = ['red', 'blue', 'olive']
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))


add_label(1.5, 0.025, "2013-Jan-12", ["color", "red"])
add_label(1.5, 0.015, "2015-Apr-16", ["color", "blue"])
add_label(3., 0.025, "2017-Jan (merged)", ["color", "olive"])


set_label("all", ['size', 18])

for i, idn in enumerate([1,2, 5]):
    plot_bkg(idn, overplot=True)
    plot_bkg_model(idn, overplot=True)
    # maybe color that gray to it fades away more
    set_curve('crv{0}'.format(7 + i), "*.color=gray")
    set_histogram('hist{0}'.format(i + 1), "*.color=gray")


# no limits placed on background, but that's not an issue as long as we only use it for plotting.
limits(X_AXIS, 0.4, 9.)
limits(Y_AXIS, 5e-5, 0.05)

# Now make the plot nicer
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ax1","minortick.visible=0 tickformat=%3.1g label.size=18 ticklabel.size=16")
log_scale(X_AXIS)
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ay1","label.size=18 offset.perpendicular=70.00 ticklabel.size=16")
set_plot_title("")

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec.pdf', ['export.clobber', True])

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
