Some of the XMM data analysis is not included in my makefile scripts.
These steps are recorded here.

 evselect table=EPIC.fits withfilteredset=Y filteredset=EPICclean.fits \
   destruct=Y keepfilteroutput=T \
   expression='Selection_Expression'

where Selection_Expression is:

    #XMMEA_EM && gti(EPICgti.fits,TIME) && (PI>150) for EPIC-MOS
    #XMMEA_EP && gti(EPICgti.fits,TIME) && (PI>150) for EPIC-pn

