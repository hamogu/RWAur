set scriptdir = $PWD

cd /melkor/d1/guenther/downdata/Chandra/RWaur

# Following Schneider et al. article here.
# RW Aur B
set srca = "circle(5:07:49.548,+30:24:05.078,0.00900')"
set bkga = "pie(5:07:49.435,+30:24:04.706,0.016666667',0.033333333',230.0018,470.0018)"
# RW Aur A (source region of same size, but much larger background region
set srcb = "circle(5:07:49.434,+30:24:04.692,0.00900')"
set bkgb = "circle(5:07:49.470,+30:24:46.246,0.41469')"

foreach obsid (14539 17644 17764 19980)
    # Dam. I forgot to ask for sub-array read-out and thus the new observations
    # suffer from pile-up.
    # Check how much and how far out that goes!
    dmcopy "${obsid}/${obsid}_evt2.fits[EVENTS][bin x=4050:4150:1,y=4050:4150:1]" $obsid/{$obsid}_fullband_image.fits option=image clob+
    pileup_map $obsid/{$obsid}_fullband_image.fits $obsid/{$obsid}_fullband_pileup.fits clob+

    # Just make raw copies of the event files - helps to look at things manually
    dmcopy "${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$srca]" "${obsid}_srca.fits" clob+
    dmcopy "${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$bkga]" "${obsid}_bkga.fits" clob+
    dmcopy "${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$srcb]" "${obsid}_srcb.fits" clob+
    dmcopy "${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$bkgb]" "${obsid}_bkgb.fits" clob+

    dmimg2jpg "${obsid}/${obsid}_evt2.fits[x=4090:4120,y=4090:4150,energy=0:800][bin sky=0.5]" "${obsid}/${obsid}_evt2.fits[x=4090:4120,y=4090:4150,energy=800:2000][bin sky=0.5]" "${obsid}/${obsid}_evt2.fits[x=4090:4120,y=4090:4150,energy=2000:8000][bin sky=0.5]" outfile="${obsid}_rgb.jpg" clob+

    # Extract lightcurves
    dmextract outfile="${obsid}_srca_lc.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$srca][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$bkga]" clob+
    dmextract outfile="${obsid}_srcb_lc.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$srcb][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=300:9000,sky=$bkgb]" clob+
    dmextract outfile="${obsid}_srca_lc_soft.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=300:1000,sky=$srca][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=300:1000,sky=$bkga]" clob+
    dmextract outfile="${obsid}_srcb_lc_soft.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=300:1000,sky=$srcb][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=300:1000,sky=$bkgb]" clob+
    dmextract outfile="${obsid}_srca_lc_hard.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=1000:9000,sky=$srca][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=1000:9000,sky=$bkga]" clob+
    dmextract outfile="${obsid}_srcb_lc_hard.fits" opt="ltc1" infile="${obsid}/${obsid}_evt2.fits[energy=1000:9000,sky=$srcb][bin time=::3600]" bkg="${obsid}/${obsid}_evt2.fits[energy=1000:9000,sky=$bkgb]" clob+

    # Extract spectra
    specextract infile="${obsid}/${obsid}_evt2.fits[sky=$srca]" bkgfile="${obsid}/${obsid}_evt2.fits[sky=$bkga]" outroot=${obsid}_A correctpsf=yes weight=no asp=${obsid}/full_asol_corrected.fits clob+
    specextract infile="${obsid}/${obsid}_evt2.fits[sky=$srcb]" bkgfile="${obsid}/${obsid}_evt2.fits[sky=$bkgb]" outroot=${obsid}_B correctpsf=yes weight=no asp=${obsid}/full_asol_corrected.fits clob+

end

combine_spectra 17764_A_grp.pi,19980_A_grp.pi 2017_A bscale_method='time' clob+
combine_spectra 17764_B_grp.pi,19980_B_grp.pi 2017_B bscale_method='time' clob+

cd $scriptdir
