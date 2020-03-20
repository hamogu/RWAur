from utils import save_conf
from shmodelshelper import save_pars, load_pars

xmmpath = '/melkor/d1/guenther/downdata/XMM/RWAur/0401870301/'

from sherpa.astro.ui import *
set_conf_opt("sigma", 1.645)
set_conf_opt('numcores', 24)  # for melkor

set_xsabund("aspl")
# Guedel et al 2014 and Schneider et al 2015 used angr

chan = '14539', '17644', '17764', '19980', '21176'