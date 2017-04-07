# run with "source ciaoscript.tcsh"

cd /melkor/d1/guenther/downdata/Chandra/RWaur
# Improve astrometry, because one of the obs is off.
# Just makes for easier plotting and defining extraction regions
# if they are all on the same coordinate system

foreach obsid (14539 17644 17764 19980)

  dmcopy "$obsid/primary/acisf*fov1*[ccd_id=7]" s3.fov clob+
  dmcopy "$obsid/primary/acisf*evt2*[ccd_id=7,sky=region(s3.fov)]" $obsid/evt2_s3.fits clob+
  fluximage $obsid/evt2_s3.fits binsize=1 bands=broad outroot=$obsid/s3 clob+
  mkpsfmap $obsid/s3_broad_thresh.img outfile=$obsid/s3_psfmap.fits energy=1.4967 ecf=0.90 clob+

  ### First, run wavdetect to find sources

  punlearn wavdetect
  wavdetect infile=$obsid/s3_broad_thresh.img psffile=$obsid/s3_psfmap.fits outfile=$obsid/{$obsid}s3_src.fits scellfile=$obsid/{$obsid}s3_scell.fits imagefile=$obsid/{$obsid}s3_imgfile.fits defnbkgfile=$obsid/{$obsid}s3_nbgd.fits regfile=$obsid/{$obsid}_s3_src.reg scales="1 2 4" clob+
  # Retain only the most significant sources with small positional errors
  # Might be better to just shift RW Aur on top if itself, but let's try this.
  dmcopy "$obsid/${obsid}s3_src.fits[filter SRC_SIGNIFICANCE=30:]" $obsid/${obsid}s3_src_filt.fits option=all clob+

end

dmmerge 14539/primary/pcadf474340808N002_asol1.fits.gz 14539/full_asol.fits clob+
dmmerge "17644/primary/pcadf545554454N001_asol1.fits.gz,17644/primary/pcadf545554606N001_asol1.fits.gz" 17644/full_asol.fits clob+
dmmerge "17764/primary/pcadf600332149N001_asol1.fits.gz,17764/primary/pcadf600332281N001_asol1.fits.gz" 17764/full_asol.fits clob+
dmmerge 19980/primary/pcadf600486674N001_asol1.fits.gz 19980/full_asol.fits clob+

# match everything to first observation
# but run on all 4 of them (the first one is matched to itself)
# to make sure event files that follow the same nameing convention are produced.

# This does not work as well as I would like, because there are too few bright
# sources in the data.

# foreach obsid (14539 17644 17764 19980)
#   wcs_match infile=$obsid/{$obsid}s3_src_filt.fits refsrcfile=14539/14539s3_src.fits outfile=$obsid/out.xform wcsfile=14539/s3_broad_thresh.img method=trans clob+

#   wcs_update infile=$obsid/full_asol.fits outfile=$obsid/full_asol_corrected.fits transformfile=$obsid/out.xform  wcsfile=14539/s3_broad_thresh.img clob+

#   dmcopy $obsid/primary/*evt2* $obsid/{$obsid}_evt2.fits op=all clob+
#   wcs_update infile=$obsid/{$obsid}_evt2.fits outfile="" transformfile=$obsid/out.xform wcsfile=14539/s3_broad_thresh.img
 
#   dmhedit $obsid/{$obsid}_evt2.fits file= op=add key=ASOLFILE value=full_asol_corrected.fits

# end

# So, instead, I look at the images and measure the offset myself by hand in ds9.
# Also, wavedetect find RW Aur as an extended source in those ObsIDs where both
# components are visible. Thus, cannot use the wavedetect output.
# Set nominal coordinates for RW Aur, X-ray bright component:
#
# This coordinates are close to correct,but just picked by hand.
# It's good enough to set extraction regions.

# wcs_update wants the offset in sky pixels. 
foreach obsid (14539 17644 17764 19980)
  dmcopy $obsid/primary/*evt2* $obsid/{$obsid}_evt2.fits op=all clob+
end

wcs_update infile=14539/full_asol.fits outfile=14539/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0. deltay=0.7
wcs_update infile=14539/14539_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0. deltay=0.7

wcs_update infile=17644/full_asol.fits outfile=17644/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=1.7 deltay=1.6
wcs_update infile=17644/17644_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=1.7 deltay=1.6

wcs_update infile=17764/full_asol.fits outfile=17764/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.1 deltay=0.2
wcs_update infile=17764/17764_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.1 deltay=0.2

wcs_update infile=19980/full_asol.fits outfile=19980/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.1 deltay=0.5
wcs_update infile=19980/19980_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.1 deltay=1.5

foreach obsid (14539 17644 17764 19980)
  dmhedit $obsid/{$obsid}_evt2.fits file= op=add key=ASOLFILE value=full_asol_corrected.fits
end


cd /melkor/d1/guenther/projects/Chandraprojects/RWAur
