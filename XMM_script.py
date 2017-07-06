# set up SAS before running this script.
# Then, run in directory with the data
from glob import glob
import numpy as np

energybands = [[200, 1000], [1000, 3000], [3000, 7000]]
gtis = ['flare.gti', 'noflare.gti']
instruments = ['EMOS1', 'EMOS2', 'EPN']
imevfiles = [ glob('*_{}_*ImagingEvts.ds'.format(inst))[0] for inst in instruments ]

with open('XMM_commands.csh', 'w') as f:

    f.write('\n### Flare and no flare images ### \n')
    for i, inst in enumerate(instruments):
        for ei, e in enumerate(energybands):
            for g in gtis:
                exp = '#XMMEA_{filt}&&(PI in [{e0}:{e1}])&&(PATTERN in [0:12])&& gti({gti},TIME)'.format(filt=inst[:2], e0=e[0], e1=e[1], gti=g)
                outname = '{}_band{}_gti{}_im.fits'.format(inst, ei, g.split('.')[0])
                f.write(' '.join(["evselect",
                                 "table={filein}:EVENTS".format(filein=imevfiles[i]),
                                 "imagebinning=binSize",
                                 "imageset={fileout}".format(fileout=outname),
                                 "withimageset=yes",
                                 "xcolumn='X'",
                                 "ycolumn='Y'",
                                 "ximagebinsize=80",
                                 "yimagebinsize=80",
                                 "expression='{exp}'\n".format(exp=exp),
                                 ]))
                f.write('\n')

    f.write('\n### edetect_chain on flare and no-flare image to find shift ####\n')
    for g in gtis:
        imsets = []
        for i, inst in enumerate(instruments):
            for ei, e in enumerate(energybands):
                imsets.append('{}_band{}_gti{}_im.fits'.format(inst, ei, g.split('.')[0]))
        f.write(' '.join(["edetect_chain",
                        "imagesets=''" + ' '.join(imsets) + "''",
                        "eventsets=''" + ' '.join(imevfiles) + "''",
                        "attitudeset={}".format(glob('*AttHk.ds')[0]),
                        "pimin=''" + ' '.join([str(e[0]) for e in energybands] * len(instruments)) + "''",
                        "pimax=''" + ' '.join([str(e[1]) for e in energybands] * len(instruments)) + "''",
                        "esp_withootset=yes",
                        "esp_ooteventset={}".format(imevfiles[-1]),
                        "eml_list=eml{}.fits\n".format(g.split('.')[0])
                        ]))
        f.write('\n')

    f.write('\n### RGS ###\n')
    f.write('rgsproc srcra=76.955428 srcdec=30.400966 withsrc=yes srclabel=mjsrc bkgcorrect=no withmlambdacolumn=yes xpsfincl=5 xpsfincl=90\n')

    f.write('\n')

    f.write('#### PN data in time intervals ###\n')
    # make gtis for spectral extraction

    tintervals = ['quiet', 'rise', 'top', 'decay1', 'decay2']
    # In in ks fomr the beginning of the lightcurve
    times = np.array([0., 19., 22., 25., 28., 35.])
    times = times * 1e3 + 288447000.

    for j, i in enumerate(tintervals):
        name = i
        expr = "'TIME>{0} && TIME<{1}'".format(times[j], times[j + 1])

        for inst in instruments:
            if inst == 'EPN':
                specchannelmax = "20479"
                spectralbinsize = 5
            else:
                specchannelmax = "11999"
                spectralbinsize = 15
            for b in ['', 'bg']:
                baseevfile = glob("1319_0401870301_{}_*_filt.fits".format(inst))[0]
                evfile = glob("RWAur_1319_0401870301_{}_*_filts{}.fits".format(inst, b))[0]
                specout = "spec_{}_{}{}".format(name, inst, b)

                f.write("evselect table={} withspectrumset=yes spectrumset={}.fits energycolumn=PI withspecranges=yes specchannelmin=0 specchannelmax={} spectralbinsize={} expression={}\n".format(evfile, specout, specchannelmax, spectralbinsize, expr))
                f.write("backscale spectrumset={specout}.fits badpixlocation={evfile}\n".format(specout=specout, evfile=evfile))
                f.write("rmfgen spectrumset={0}.fits rmfset={0}.rmf\n".format(specout))
                f.write("arfgen spectrumset={0}.fits arfset={0}.arf withrmfset=yes rmfset={0}.rmf badpixlocation={1} detmaptype=psf\n".format(specout, baseevfile))

            basename = "spec_{}_{}".format(name, inst)
            f.write('rm {}.15grp\n'.format(basename))
            f.write('grppha {0}.fits {0}.15grp comm="chkey respfile {0}.rmf & chkey backfile {0}bg.fits & chkey ancrfile {0}.arf & group min 15 & exit"\n'.format(basename))
