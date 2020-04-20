# run with "source ciaoscript.tcsh"

cd /melkor/d1/guenther/downdata/Chandra/RWaur

chandra_repro indir="*" outdir=''

# Improve astrometry, because one of the obs is off.
# Just makes for easier plotting and defining extraction regions
# if they are all on the same coordinate system

#foreach obsid (14539 17644 17764 19980 21176 22323 23100 23101 23102)
#
#  dmcopy "$obsid/repro/acisf*fov1*[ccd_id=7]" s3.fov clob+
#  dmcopy "$obsid/repro/acisf*evt2*[ccd_id=7,sky=region(s3.fov)]" $obsid/evt2_s3.fits clob+
#  fluximage $obsid/evt2_s3.fits binsize=1 bands=broad outroot=$obsid/s3 clob+
#  mkpsfmap $obsid/s3_broad_thresh.img outfile=$obsid/s3_psfmap.fits energy=1.4967 ecf=0.90 clob+
#
#  ### First, run wavdetect to find sources
#
#  punlearn wavdetect
#  wavdetect infile=$obsid/s3_broad_thresh.img psffile=$obsid/s3_psfmap.fits outfile=$obsid/{$obsid}s3_src.fits scellfile=$obsid/{$obsid}s3_scell.fits imagefile=$obsid/{$obsid}s3_imgfile.fits defnbkgfile=$obsid/{$obsid}s3_nbgd.fits regfile=$obsi$d/{$obsid}_s3_src.reg scales="1 2 4" clob+
#  # Retain only the most significant sources with small positional errors
#  # Might be better to just shift RW Aur on top if itself, but let's try this.
#  dmcopy "$obsid/${obsid}s3_src.fits[filter SRC_SIGNIFICANCE=30:]" $obsid/${obsid}s3_src_filt.fits option=all clob+
#
#end

foreach obsid (14539 17644 17764 19980 21176 22323 23100 23101 23102)
  dmmerge "@${obsid}/repro/acisf${obsid}_asol1.lis" $obsid/full_asol.fits clob+
  dmcopy $obsid/repro/*evt2* $obsid/{$obsid}_evt2.fits op=all clob+
end

# match everything to first observation
# but run on all 4 of them (the first one is matched to itself)
# to make sure event files that follow the same naming convention are produced.

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
# Set nominal coordinates for RW Aur B, X-ray bright component:
#
# These coordinates are close to correct, but just picked by hand.
# It's good enough to set extraction regions.
# Place a region by hand on RW Aur B and use Analysis->CIAO->Statistics->centroid
# or ds9 Region-> Centroid
# These numbers depend little (< 0.1 pixel) on the hand-picked position for 
# reasonable starting values
# Measured Centroids for RW Aur B are in the table below
# Coordinates that Christian used for RW Aur B: 5:07:49.4340 +30:24:04.692
# All values in the table in "physical"
# ObsID centr_ra centr_dec christian_ra christian_dec
# 14539 4119.8450901 4106.1350137 4120.033 4106.6725
# 17644 4129.748604 4119.5693573  4131.3496 4121.2033
# 17764 4120.9990768 4113.3334865  4121.1913 4113.5425
# 19980 4121.449809 4113.765731 4121.6729 4115.1893
# 21176 4071.3564091 4096.0130464 4071.6955 4097.8434
# 22323 4101.9668 4137.2438 4102.6079 4136.9451
# 23100 4105.7266 4127.2515 4105.882 4128.069
# 23101 4106.0097 4126.5709 4106.1227 4127.3473
# 23102 4106.4298 4125.1914 4106.5561 4126.0634
# From this I can calculate pixel offset

wcs_update infile=14539/full_asol.fits outfile=14539/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.19 deltay=0.54
wcs_update infile=14539/14539_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.19 deltay=0.54

wcs_update infile=17644/full_asol.fits outfile=17644/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=1.6 deltay=1.63
wcs_update infile=17644/17644_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=1.6 deltay=1.63

wcs_update infile=17764/full_asol.fits outfile=17764/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.2 deltay=0.21
wcs_update infile=17764/17764_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.2 deltay=0.21

wcs_update infile=19980/full_asol.fits outfile=19980/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.22 deltay=1.42
wcs_update infile=19980/19980_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.22 deltay=1.42

wcs_update infile=21176/full_asol.fits outfile=21176/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.34 deltay=1.83
wcs_update infile=21176/21176_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.34 deltay=1.83

wcs_update infile=22323/full_asol.fits outfile=22323/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.64 deltay=-0.30
wcs_update infile=22323/22323_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.64 deltay=-0.30

wcs_update infile=23100/full_asol.fits outfile=23100/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.16 deltay=0.82
wcs_update infile=23100/23100_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.16 deltay=0.82

wcs_update infile=23101/full_asol.fits outfile=23101/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.11 deltay=0.78
wcs_update infile=23101/23101_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.11 deltay=0.78

wcs_update infile=23102/full_asol.fits outfile=23102/full_asol_corrected.fits  wcsfile=14539/s3_broad_thresh.img clob+ transformfile="" deltax=0.13 deltay=0.87
wcs_update infile=23102/23102_evt2.fits outfile="" wcsfile=14539/s3_broad_thresh.img  transformfile="" deltax=0.13 deltay=0.87


foreach obsid (14539 17644 17764 19980 21176 22323 23100 23101 23102)
  dmhedit $obsid/{$obsid}_evt2.fits file= op=add key=ASOLFILE value=full_asol_corrected.fits
end


cd /melkor/d1/guenther/projects/Chandraprojects/RWAur
