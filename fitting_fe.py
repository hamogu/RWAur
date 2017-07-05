import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from utils import save_conf


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

group_counts(1, 1)
group_counts(2, 1)
group_counts(3, 5)


set_xsabund("angr")  # for consistency with Guedel et al 2014 and Schneider et al 2015
set_source(1, xsphabs.a1 * xsvapec.v1)
set_source(2, a1 * v1)
set_source(3, a1 * v1)
v1.Fe.frozen=False
notice(3, 9.)

set_stat("cash")
a1.nH = 38
v1.kT = 1.15
v1.Fe = 10
v1.norm = 0.006
fit(1,2)

set_conf_opt("sigma", 1.645)
conf(1,2)
save_conf('spec_fe.json', energy_flux=1, absorbpars=[a1.nH])


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
limits(X_AXIS, 6.4, 7.)
set_axis("ax1","minortick.visible=1 tickformat=%3.2g ticklabel.size=20")
set_axis("ay1","ticklabel.size=20")
v1.kT = 5.5
v1.kT.frozen = True
fit(1, 2)
plot_fit(3, overplot=True)
set_curve('crv4', "*.color=default line.style=longdash")

# Now back to the big plot and add the dashed line there, too.
current_plot("plot1")
plot_fit(3, overplot=True)
set_curve('crv4', "*.color=default line.style=longdash")


print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_17.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/spec_17.pdf', ['export.clobber', True])
