import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from shmodelshelper import load_pars

xmmpath = '/melkor/d1/guenther/downdata/XMM/RWAur/0401870301/'

load_data(1, '14539_B_grp.pi')
ignore_bad(1)

load_data(11, xmmpath + 'RWAur_1319_0401870301_EPN_S003_spec.15grp')

group_counts(1, 25)
group_counts(11, 25)

ignore(None, .2)
ignore(9., None)

for i in [1, 11]:
    set_model(i, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))

for v in [v2, v3]:
    for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
        setattr(v, elem, getattr(v1, elem))

v1.Si = v1.Fe
v1.Mg = v1.Fe

load_pars('RWAurXMM.pars', [a1, v1, v2, v3])

plot_fit(11)

load_pars('RWAurBChan1.pars', [a1, v1, v2, v3])
plot_fit(1, overplot=True)

log_scale()
set_curve('crv1', "*.color=olive")
set_curve('crv2', "*.color=olive")

set_curve('crv3', "*.color=orange")
set_curve('crv4', "*.color=orange")

add_label(3., 0.5, "XMM 2007", ["color", "olive"])
add_label(3., 0.5 * 0.5, "RW Aur AB", ["color", "olive"])
add_label(.5, 0.003, "Chandra 2013", ["color", "orange"])
add_label(.5, 0.5*0.003, "RW Aur B", ['color', 'orange'])
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

print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/specB.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/specB.pdf', ['export.clobber', True])
