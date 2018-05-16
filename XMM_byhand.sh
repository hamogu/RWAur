Some of the XMM data analysis is not included in my makefile scripts.
These steps are recorded here.

 evselect table=EPIC.fits withfilteredset=Y filteredset=EPICclean.fits \
   destruct=Y keepfilteroutput=T \
   expression='Selection_Expression'

where Selection_Expression is:

    #XMMEA_EM && gti(EPICgti.fits,TIME) && (PI>150) for EPIC-MOS
    #XMMEA_EP && gti(EPICgti.fits,TIME) && (PI>150) for EPIC-pn

evselect rateset=PN_0390_lc.fits withrateset=true table=RWAur_1319_0401870301_EPN_S003_filts.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=600 expression="PI in [300:9000]"
evselect rateset=PN_0310_lc.fits withrateset=true table=RWAur_1319_0401870301_EPN_S003_filts.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=600 expression="PI in [300:1000]"
evselect rateset=PN_1090_lc.fits withrateset=true table=RWAur_1319_0401870301_EPN_S003_filts.fits makeratecolumn=yes maketimecolumn=yes timecolumn=TIME timebinsize=600 expression="PI in [1000:9000]"

omfchain timebinsize=600

setenv SAS_CCF "ccf.cif"
setenv SAS_ODF ODF

rgsproc xpsfincl=70

rgsproc entrystage=3:filter auxgtitables=flare.gti xpsfincl=70

setenv SAS_ODF /melkor/d1/guenther/downdata/XMM/RWAur/0401870301/ODF
setenv SAS_CCF /melkor/d1/guenther/downdata/XMM/RWAur/0401870301/ccf.cif


evselect table=P0401870301R1S004EVENLI0000.FIT:EVENTS withimageset=yes imageset='my_spatial1.fit' xcolumn='BETA_CORR' ycolumn='XDSP_CORR'

