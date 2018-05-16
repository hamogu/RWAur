# Copy and paste from the other scripts to make figures for XMM proposal

import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from shmodelshelper import load_pars

xmmpath = '/melkor/d1/guenther/downdata/XMM/RWAur/0401870301/'

load_data(1, '14539_A_grp.pi')
ignore_bad(1)

load_data(2, '14539_B_grp.pi')
ignore_bad(2)


load_data(11, xmmpath + 'RWAur_1319_0401870301_EPN_S003_spec.15grp')
load_data(12, xmmpath + 'RWAur_noflare_1319_0401870301_EPN_S003_spec.15grp')


group_counts(1, 25)
group_counts(2, 25)
group_counts(11, 25)
group_counts(12, 25)

ignore(None, .2)
ignore(9., None)

for i in [1, 2, 11, 12]:
    set_model(i, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))

for v in [v2, v3]:
    for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
        setattr(v, elem, getattr(v1, elem))

v1.Si = v1.Fe
v1.Mg = v1.Fe

load_pars('RWAurXMM.pars', [a1, v1, v2, v3])

fit(11)
plot_fit(11)

fit(12)
plot_fit(12, overplot=True)

fit(2)
plot_fit(2, overplot=True)  # Assuming that the XMM fit works here, too.

load_pars('RWAurBChan1.pars', [a1, v1, v2, v3])
fit(1)
plot_fit(1, overplot=True)

log_scale()
set_curve('crv1', "*.color=olive")
set_curve('crv2', "*.color=olive")

set_curve('crv3', "*.color=olive")
set_curve('crv4', "*.color=olive")

set_curve('crv5', "*.color=orange")
set_curve('crv6', "*.color=orange")

set_curve('crv7', "*.color=blue")
set_curve('crv8', "*.color=blue")


add_label(3., 0.5, "XMM 2007", ["color", "olive"])
add_label(3., 0.5 * 0.5, "RW Aur AB", ["color", "olive"])
add_label(.5, 0.002, "Chandra 2013", ["color", "orange"])
add_label(.5, 0.5*0.002, "RW Aur B", ['color', 'orange'])
add_label(1.3, 0.0003, "Chandra 2013", ["color", "blue"])
add_label(1.3, 0.5*0.0003, "RW Aur A", ['color', 'blue'])

set_label("all", ['size', 30])

limits(X_AXIS, 0.4, 9.)
#limits(Y_AXIS, 5e-5, 0.05)
# Now make the plot nicer
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ax1","minortick.visible=0 tickformat=%3.1g label.size=30 ticklabel.size=26 offset.perpendicular=60")
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ay1","label.size=30 offset.perpendicular=70.00 ticklabel.size=26")
set_plot_title("")

plot = get_plot()
plot.rightmargin = 0.01
plot.topmargin = 0.01
plot.bottommargin = 0.15
set_plot(plot)

print_window('/melkor/d1/guenther/Dropbox/my_proposals/XMM/RW_Aur/spec2013.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_proposals/XMM/RW_Aur/spec2013.pdf', ['export.clobber', True])













### Now 2017 ###
xmmpath = '/melkor/d1/guenther/downdata/XMM/canned/'
jsonfiles = '/melkor/d1/guenther/Dropbox/my_articles/RWAur/'

load_data(1, '17764_A_grp.pi')
ignore_bad(1)

load_data(2, '17764_B_grp.pi')
ignore_bad(2)


ignore(None, .2)
ignore(9., None)


group_counts(1, 10)
group_counts(2, 10)

set_model(1, xsphabs.a1 * xsvapec.v1)
set_model(2, xsphabs.a21 * (xsvapec.v21 + xsvapec.v22 + xsvapec.v23))

load_pars('RWAurBChan3.pars', [a21, v21, v22, v23])
fit(2)

a1.nH = 38.
v1.Fe = 10
v1.kT = 1.15
v1.norm = 0.006438716657473479

set_model(11, xsphabs.a1 * xsvapec.v1 +
          xsphabs.a21 * (xsvapec.v21 + xsvapec.v22 + xsvapec.v23))
fake_pha(11, xmmpath + 'pn-med-5.arf.gz', xmmpath + 'pn-med-5.rmf.gz', 25000)

group_counts(11, 25)

plot_fit(11)

plot_fit(2, overplot=True)
plot_fit(1, overplot=True)

log_scale()
set_curve('crv1', "*.color=olive")
set_curve('crv2', "*.color=olive")

set_curve('crv3', "*.color=orange")
set_curve('crv4', "*.color=orange")

set_curve('crv5', "*.color=blue")
set_curve('crv6', "*.color=blue")


add_label(2., 0.2, "XMM predicted", ["color", "olive"])
add_label(2., 0.2 * 0.5, "RW Aur AB", ["color", "olive"])
add_label(.7, 0.003, "Chandra 2017", ["color", "orange"])
add_label(.7, 0.5*0.003, "RW Aur B", ['color', 'orange'])
add_label(.8, 0.0003, "Chandra 2017", ["color", "blue"])
add_label(.8, 0.5*0.0003, "RW Aur A", ['color', 'blue'])

set_label("all", ['size', 30])

limits(X_AXIS, 0.4, 9.)
limits(Y_AXIS, 1e-4, 0.4)
# Now make the plot nicer
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ax1","minortick.visible=0 tickformat=%3.1g label.size=30 ticklabel.size=26 offset.perpendicular=60")
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ay1","label.size=30 offset.perpendicular=70.00 ticklabel.size=26")
set_plot_title("")

plot = get_plot()
plot.rightmargin = 0.01
plot.topmargin = 0.01
plot.bottommargin = 0.15
set_plot(plot)

print_window('/melkor/d1/guenther/Dropbox/my_proposals/XMM/RW_Aur/spec2017.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_proposals/XMM/RW_Aur/spec2017.pdf', ['export.clobber', True])
