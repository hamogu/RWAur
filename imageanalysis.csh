# run in tcsh with > source imageanalysis.csh
set scriptdir = $PWD

cd /melkor/d1/guenther/downdata/Chandra/RWaur

# Following Schneider et al. article here.
# RW Aur A
set srca = "circle(5:07:49.548,+30:24:05.078,0.00900')"
set bkga = "pie(5:07:49.435,+30:24:04.706,0.016666667',0.033333333',230.0018,470.0018)"
# RW Aur B (source region of same size, but much larger background region
set srcb = "circle(5:07:49.434,+30:24:04.692,0.00900')"
set bkgb = "circle(5:07:49.470,+30:24:46.246,0.41469')"

foreach obsid (14539 17644 17764 19980 21176 22323 23100 23101 23102)
    # Dam. I forgot to ask for sub-array read-out in 2015 
    # Check how much pile up that had!
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
    punlearn specextract
    punlearn ardlib
    specextract infile="${obsid}/${obsid}_evt2.fits[sky=$srca]" bkgfile="${obsid}/${obsid}_evt2.fits[sky=$bkga]" outroot=${obsid}_A correctpsf=yes weight=no asp=${obsid}/full_asol_corrected.fits badpixfile="${obsid}/repro/*bpix1.fits" clob+
    specextract infile="${obsid}/${obsid}_evt2.fits[sky=$srcb]" bkgfile="${obsid}/${obsid}_evt2.fits[sky=$bkgb]" outroot=${obsid}_B correctpsf=yes weight=no asp=${obsid}/full_asol_corrected.fits badpixfile="${obsid}/repro/*bpix1.fits" clob+

    # Extract radial profiles
    # Not sure if the centroiding was done well enough for this to be useful, but visual inspection
    # of the annuli regions in ds9 looks good
    dmcopy "${obsid}/${obsid}_evt2.fits[exclude sky=region(${scriptdir}/RWAurB_annulus_subtr_A.reg)]" ${obsid}/${obsid}_evt2_exclA.fits clob+
    punlearn dmextract
    dmextract "${obsid}/${obsid}_evt2_exclA.fits[bin sky=@${scriptdir}/RWAurB_annulus.reg]" ${obsid}_rprofile.fits bkg="${obsid}/${obsid}_evt2_exclA.fits[bin sky=@${scriptdir}/RWAurB_annulus_bkg.reg]" opt=generic clob+

end


# Combine 2017 spectra. This is not used for analysis, only for display purposes.
combine_spectra 17764_A_grp.pi,19980_A_grp.pi 2017_A bscale_method='counts' clob+
combine_spectra 17764_B_grp.pi,19980_B_grp.pi 2017_B bscale_method='counts' clob+

# Combine 2019 spectra. This is not used for analysis, only for display purposes.
combine_spectra 22323_A_grp.pi,23100_A_grp.pi,23101_A_grp.pi,23102_A_grp.pi 2019_A bscale_method='counts' clob+
combine_spectra 22323_B_grp.pi,23100_B_grp.pi,23101_B_grp.pi,23102_B_grp.pi 2019_B bscale_method='counts' clob+



# Split extraction of 2017 (1) steady and flare

dmcopy "17764/17764_evt2.fits[time=600332393:600362393]" 17764/17764_evt2_preflare.fits
dmcopy "17764/17764_evt2.fits[time=600362393:600382393]" 17764/17764_evt2_flare.fits

specextract infile="17764/17764_evt2_preflare.fits[sky=$srca]" bkgfile="17764/17764_evt2_preflare.fits[sky=$bkga]" outroot=17764_A_preflare correctpsf=yes weight=no asp=17764/full_asol_corrected.fits badpixfile="17764/repro/*bpix1.fits" clob+
specextract infile="17764/17764_evt2_preflare.fits[sky=$srcb]" bkgfile="17764/17764_evt2_preflare.fits[sky=$bkgb]" outroot=17764_B_preflare correctpsf=yes weight=no asp=17764/full_asol_corrected.fits badpixfile="17764/repro/*bpix1.fits" clob+

specextract infile="17764/17764_evt2_flare.fits[sky=$srca]" bkgfile="17764/17764_evt2_flare.fits[sky=$bkga]" outroot=17764_A_flare correctpsf=yes weight=no asp=17764/full_asol_corrected.fits badpixfile="17764/repro/*bpix1.fits" clob+
specextract infile="17764/17764_evt2_flare.fits[sky=$srcb]" bkgfile="17764/17764_evt2_flare.fits[sky=$bkgb]" outroot=17764_B_flare correctpsf=yes weight=no asp=17764/full_asol_corrected.fits badpixfile="17764/repro/*bpix1.fits" clob+

# Split extraction of 2018 into steady and flare

dmcopy "21176/21176_evt2.fits[exclude time=659495000:659508000]" 21176/21176_evt2_noflare.fits
dmcopy "21176/21176_evt2.fits[time=659495000:659508000]" 21176/21176_evt2_flare.fits

specextract infile="21176/21176_evt2_noflare.fits[sky=$srca]" bkgfile="21176/21176_evt2_noflare.fits[sky=$bkga]" outroot=21176_A_noflare correctpsf=yes weight=no asp=21176/full_asol_corrected.fits badpixfile="21176/repro/*bpix1.fits" clob+
specextract infile="21176/21176_evt2_noflare.fits[sky=$srcb]" bkgfile="21176/21176_evt2_noflare.fits[sky=$bkgb]" outroot=21176_B_noflare correctpsf=yes weight=no asp=21176/full_asol_corrected.fits badpixfile="21176/repro/*bpix1.fits" clob+

specextract infile="21176/21176_evt2_flare.fits[sky=$srca]" bkgfile="21176/21176_evt2_flare.fits[sky=$bkga]" outroot=21176_A_flare correctpsf=yes weight=no asp=21176/full_asol_corrected.fits badpixfile="21176/repro/*bpix1.fits" clob+
specextract infile="21176/21176_evt2_flare.fits[sky=$srcb]" bkgfile="21176/21176_evt2_flare.fits[sky=$bkgb]" outroot=21176_B_flare correctpsf=yes weight=no asp=21176/full_asol_corrected.fits badpixfile="21176/repro/*bpix1.fits" clob+

# Process optical monitor data
foreach obsid (17644 17764 19980 21176 22323 23100 23101 23102)

cd ${obsid}/secondary/aspect
gunzip *adat71.fits.gz
ls -1 *adat71.fits > adat71.lis
dmmerge infile=@adat71.lis outfile=pcad_adat71.fits clobber=yes
monitor_photom infile=pcad_adat71.fits outfile="../../../monitor_${obsid}_lc.fit" verbose=1 clobber=yes
cd ../../../

end

cd $scriptdir


