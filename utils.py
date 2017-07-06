from os.path import join
import json
from sherpa.astro import ui

articlepath = '/melkor/d1/guenther/Dropbox/my_articles/RWAur'


def save_conf(filename, energy_flux=None, absorbpars=[]):
    '''
    Parameters
    ----------
    filename : string
    energy_flux : string or integer
        Identifier of Sherpa model for which the energy flux will be calculated.
    absorbpars : sherpa parameter instances
        These parameters are set to 0 before the flux is calculated.
    '''
    confres = ui.get_conf_results()
    fitres = ui.get_fit_results()

    if energy_flux is not None:
        oldval = [getattr(a, 'val') for a in absorbpars]
        for a in absorbpars:
            setattr(a, 'val', 0.)
        energy_flux = ui.calc_energy_flux(0.3, 9., energy_flux)
        for a, v in zip(absorbpars, oldval):
            setattr(a, 'val', v)

    with open(join(articlepath, filename), 'w') as f:
        json.dump({'name': confres.parnames, 'val': confres.parvals,
                   'up': confres.parmaxes, 'down': confres.parmins,
                   'redchi2': fitres.rstat, 'dof': fitres.dof,
                   'flux': energy_flux}, f)
