import sys
sys.path.append('/melkor/d1/guenther/projects/Chandraprojects/RWAur/')
from base_fit import *

#tintervals = ['quiet', 'rise', 'top', 'decay1', 'decay2']
tintervals = ['basal', 'fullflare']
colors = ['black', 'red', 'olive', 'blue', 'magenta']
for i, name in enumerate(tintervals):
    load_data(i * 10 + 1, xmmpath + "spec_{}_EPN.15grp".format(name))
    load_data(i * 10 + 2, xmmpath + "spec_{}_EMOS1.15grp".format(name))
    load_data(i * 10 + 3, xmmpath + "spec_{}_EMOS2.15grp".format(name))

for i in range(1, len(tintervals) + 1):
    group_counts(i, 20)

ignore(None, .2)
ignore(9., None)

# for i in range(0, len(tintervals)):
#     plot_data(i * 10 + 1, overplot=(i > 0))
#     if i > 0:
#         set_curve('crv{:d}'.format(i+1), "*.color=" + colors[i])

# for i in range(1, len(tintervals) + 1):
#     set_model(i, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))



# for v in [v2, v3]:
#     for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
#         setattr(v, elem, getattr(v1, elem))


# v1.Fe.frozen = False
# v1.Si = v1.Fe
# v1.Mg = v1.Fe
# v1.Ne.frozen = False

# # Set to reasonable values before fit to speed convergence
# a1.nH = 0.2
# v1.kT = 0.3
# v2.kT = 1.5
# v3.kT = 5.

# v1.kT.frozen = True
# v2.kT.frozen = True
# v3.kT.frozen = True
# a1.nH.frozen = True
# v1.Ne = 2.3
# v1.Ne.frozen = False
# v1.Fe = 0.6
# v1.Fe.frozen = False

# for i in range(len(tintervals)):
#     set_model(i * 10 + 1, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
#     set_model(i * 10 + 2, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
#     set_model(i * 10 + 3, xsphabs.a1 * (xsvapec.v1 + xsvapec.v2 + xsvapec.v3))
#     fit(i * 10 + 1, i*10+2,i*10+3)

# After this general thing, set up a model for just basal and flare
# and then couple some of the parameters
for i in [1, 2, 3]:
    set_model(i, xsphabs.a1 * (xsvapec.v11 + xsvapec.v12))

for i in [11, 12, 13]:
    set_model(i, xsphabs.a2 * (xsvapec.v21 + xsvapec.v22))

for t1, t2 in [(v11, v12), (v21, v22)]:
    for elem in ['C', 'N', 'O','Ne', 'Fe', 'Si', 'Mg']:
        setattr(t2, elem, getattr(t1, elem))

for v in [v11, v21]:
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

fit(1,2,3,11,12,13)
conf(1,2,3,11,12,13)

save_pars('RWAurXMMflare.pars', [a1, v21, v22], clobber=True)

plot_fit(1)
plot_fit(11, overplot=True)
set_curve('crv2', "*.color=default")
set_curve('crv3', "*.color=red")
set_curve('crv4', "*.color=orange")
set_plot_title("")

log_scale()

add_label(.5, 0.002, "XMM quiescent", ["color", "default"])
add_label(3., 1, "XMM flare", ["color", "red"])
add_label(0.5, .0008, "RW Aur AB unresolved", ["color", "default"])
set_label("all", ['size', 30])

plot = get_plot()
plot.rightmargin = 0.01
plot.topmargin = 0.01
plot.bottommargin = 0.15
set_plot(plot)
set_axis("ax1","minortick.visible=0 tickformat=%3.1g label.size=30 ticklabel.size=26 offset.perpendicular=60")
set_arbitrary_tick_positions("ax1",[5,3,2,1,0.5,8],["5","3","2","1","0.5","8"])
set_axis("ay1","label.size=30 offset.perpendicular=70.00 ticklabel.size=26")


print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/XMM.png', ['export.clobber', True])
print_window('/melkor/d1/guenther/Dropbox/my_articles/RWAur/XMM.pdf', ['export.clobber', True])


Datasets              = 1, 2, 3, 11, 12, 13
Method                = levmar
Statistic             = chi2gehrels
Initial fit statistic = 1274.7
Final fit statistic   = 1176.94 at function evaluation 61
Data points           = 1735
Degrees of freedom    = 1726
Probability [Q-value] = 1
Reduced statistic     = 0.681886
Change in statistic   = 97.7653
   a1.nH          0.262331
   v11.kT         0.776204
   v11.Ne         1.17213
   v11.Fe         0.117633
   v11.norm       0.000455369
   v12.kT         6.07082
   v12.norm       0.000197856
   v21.norm       0.0019401
   v22.norm       0.00545964
sherpa-34> conf(1,2,3,11,12,13)

confidence 1.645-sigma (90.003%) bounds:
   Param            Best-Fit  Lower Bound  Upper Bound
   -----            --------  -----------  -----------
   a1.nH            0.262331   -0.0126665    0.0135354
   v11.kT           0.776204   -0.0454703    0.0423354
   v11.Ne            1.17213    -0.366167     0.461862
   v11.Fe           0.117633   -0.0255853    0.0333578
   v11.norm      0.000455369 -7.02599e-05  7.21715e-05
   v12.kT            6.07082    -0.276559     0.289549
   v12.norm      0.000197856 -2.04143e-05  2.03066e-05
   v21.norm        0.0019401 -0.000381759  0.000425518
   v22.norm       0.00545964  -0.00012211  0.000115172
