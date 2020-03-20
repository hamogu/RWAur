import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from base_fit import *

### Fitting Chandra data from B
for i, obsid in enumerate(['14539', '17644', '17764', '19980', '21176']):
    load_data(i + 1, obsid + '_B_grp.pi')
    load_bkg(i + 1, obsid + '_B_bkg.pi')

load_data(6, '2017_B_src.pi')
load_bkg(6, '2017_B_bkg.pi')

for i in [1, 2, 3, 4, 5]:
    ignore_bad(i)


ignore(None, 0.3)
ignore(9., None)

for i in [1, 2, 3, 4, 5]:
    group_counts(i, 15)


#for i in [3,4,5]:
#    set_pileup_model(i, jdpileup.jdp)


set_model(1, xsphabs.a1 * (xsvapec.v11 + xsvapec.v12))
set_model(2, xsphabs.a2 * (xsvapec.v21 + xsvapec.v22))
set_model(3, xsphabs.a3 * (xsvapec.v31 + xsvapec.v32))
set_model(4, xsphabs.a3 * (xsvapec.v31 + xsvapec.v32))
set_model(6, xsphabs.a3 * (xsvapec.v31 + xsvapec.v32))
set_model(5, xsphabs.a3 * (xsvapec.v41 + xsvapec.v42))

for t1, t2 in [(v11, v12), (v21, v22), (v31, v32), (v41, v42)]:
    for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
        setattr(t2, elem, getattr(t1, elem))

for v in [v11, v21, v31, v41]:
    v.Fe.frozen = False
    v.Si = v.Fe
    v.Mg = v.Fe
    v.Ne.frozen = False
    # and set some reasonable starting value to speed convergence
    v.kT = 1.
    v.Fe = 0.5
    v.Ne = 4

a2.nH = a1.nH
v21.Ne = v11.Ne
v21.Fe = v11.Fe
v21.kT = v11.kT
v22.kT = v12.kT
a3.nH = a1.nH
v31.Ne = v11.Ne
v31.Fe = v11.Fe
v31.kT = v11.kT
v32.kT = v12.kT

fit(1, 2, 3, 4, 5)
conf(1, 2, 3, 4, 5)

save_pars('RWAurB.pars', [a1, v11, v12, v21,v22, v31, v32, v41, v42], clobber=True)


for i in [1,2,3,4,5, 6]:
    subtract(i)

plot_fit(1)
log_scale()
plot_fit(2, overplot=True)
plot_fit(6, overplot=True)
plot_fit(5, overplot=True)

colors = ['red', 'blue', 'default']
for i, c in enumerate(colors):
    crv = 'crv{0}'.format(2*i+1)
    set_curve(crv, "*.color={}".format(c))
    crv = 'crv{0}'.format(2*i+2)
    set_curve(crv, "*.color={}".format(c))

add_label(.7, 0.001 * .6**2, "2013-Jan-12", ["color", "red"])
add_label(.7, 0.001 * 0.6, "2015-Apr-16", ["color", "blue"])
add_label(.7, 0.001, "2017-Jan (merged)", ["color", "default"])
set_label("all", ['size', 30])

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

limits(X_AXIS, 0.4, 5.1)
limits(Y_AXIS, 0.0003, 0.12)

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/specB.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/specB.pdf', ['export.clobber', True])
