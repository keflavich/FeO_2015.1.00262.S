# You should run this with CASA 4.6

thesteps = []
step_title = {0: 'Image continuum bandpass',
              1: 'Image continuum OrionBullets',
              2: 'Image line FeO_J=5-4_O=0_p=-+ 5',
              3: 'Image line FeO_J=5-4_O=1_p=+-',
              4: 'Image line KCl v = 0 20-19',
              5: 'Image line FeO_J=5-4_O=3',
              6: 'Image line FeO_J=5-4_O=4 rep. spw.',
              7: 'Export FITS images'}

try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps

thems = 'uid___A002_Xb70397_X9f06.ms.split.cal'

print thems

myimages = set([])

v0 = '154.060GHz' # FeO_J=5-4_O=3
v1 = '153.600GHz' # KCl v = 0 20-19
v2 = '156.660GHz' # FeO_J=5-4_O=0_p=-+ 
v3 = '155.810GHz' # FeO_J=5-4_O=1_p=+-
v4 = '153.135GHz' # FeO_J=5-4_O=4 rep. spw 


# Image continuum of the bandpass calibrator 
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf J0423-0120_cont.*')
  clean(vis= thems,
        imagename='J0423-0120_cont',
        field="J0423-0120",
        spw ="",
        mode="mfs",
        nterms=2,
        niter=100,
        threshold="0.1mJy",
        psfmode="clark",
        interactive=True,
        mask = [],
        imsize=[300, 300],
        cell="0.13arcsec",
        outframe='LSRK',
        weighting="briggs",
        robust = 0.5, 
        usescratch=False)

  os.system('mv J0423-0120_cont.image.tt0 J0423-0120_cont.image') 

# Image continuum of the target source 
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf OrionBullets_cont.*')
  clean(vis= thems,
        imagename='OrionBullets_cont',
        field="OrionBullets",
        spw ="4~8",
        mode="mfs",
        nterms=2,
        niter=100,
        threshold="0.1mJy",
        psfmode="clark",
        interactive=True,
        mask = [],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        weighting="briggs",
        robust = 0.5, 
        usescratch=False)

  os.system('mv OrionBullets_cont.image.tt0 OrionBullets_cont.image') 

#RESULTS: 0.37" x 0.32"  RMS = 35 uJy

# Image spw 5
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf OrionBullets_FeO_5_4_0*')
  clean(vis= thems,
        imagename= 'OrionBullets_FeO_5_4_0',
        field="OrionBullets",
        spw="5",
        mode="velocity",
        width='477.982 m/s',
        start='-100km/s',
        interpolation="linear",
        interactive=True,
        mask=[],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        restfreq= v2,
        threshold ='3.50 mJy',
        weighting="briggs",
        robust=0.5)

#RESULTS: 0.38" x 0.33"  RMS = 3.2 mJy, no detection

# Image spw 6
mystep = 3
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep] 
  os.system('rm -rf OrionBullets_FeO_5_4_1*')
  clean(vis= thems,
        imagename= 'OrionBullets_FeO_5_4_1',
        field="OrionBullets",
        spw="6",
        mode="velocity",
        width='477.982 m/s',
        start='-100km/s',
        interpolation="linear",
        interactive=True,
        mask=[],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        restfreq= v3,
        threshold ='3.50 mJy',
        weighting="briggs",
        robust=0.5)

#RESULTS: 0.38" x 0.33"  RMS = 1.6 mJy, no detection

# Image spw 7
mystep = 4
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]
  os.system('rm -rf OrionBullets_KCl*')
  clean(vis= thems,
        imagename= 'OrionBullets_KCl',
        field="OrionBullets",
        spw="7",
        mode="velocity",
        width='477.982 m/s',
        start='-100km/s',
        interpolation="linear",
        interactive=True,
        mask=[],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        restfreq= v1,
        threshold ='3.50 mJy',
        weighting="briggs",
        robust=0.5)

#RESULTS: 0.38" x 0.33"  RMS = 1.5 mJy, no detection

# Image spw 8
mystep = 5
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]
  os.system('rm -rf OrionBullets_FeO_5_4_3*')
  clean(vis= thems,
        imagename= 'OrionBullets_FeO_5_4_3',
        field="OrionBullets",
        spw="8",
        mode="velocity",
        width='477.982 m/s',
        start='-100km/s',
        interpolation="linear",
        interactive=True,
        mask=[],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        restfreq= v0,
        threshold ='3.50 mJy',
        weighting="briggs",
        robust=0.5)


#RESULTS: 0.38" x 0.33"  RMS = 1.7 mJy, no detection


# Image spw 4 rep. spw

mystep = 6
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]
  os.system('rm -rf OrionBullets_FeO_5_4_4*')
  clean(vis= thems,
        imagename= 'OrionBullets_FeO_5_4_4',
        field="OrionBullets",
        spw="4",
        mode="velocity",
        width='477.982 m/s',
        start='-100km/s',
        interpolation="linear",
        interactive=True,
        mask=[],
        imsize=[500, 500],
        cell="0.13arcsec",
        outframe='LSRK',
        restfreq= v4,
        threshold ='3.50 mJy',
	uvtaper=T, outertaper='0.4arcsec',weighting='natural',restoringbeam='0.5arcsec')
        #weighting="briggs",
        #robust=0.5)

#RESULTS: 0.38" x 0.34"  RMS = mJy, no detection

# export fits
mystep = 7
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  myimages.add('OrionBullets_cont')
  myimages.add('OrionBullets_FeO_5_4_4')
  myimages.add('OrionBullets_FeO_5_4_3')
  myimages.add('OrionBullets_FeO_5_4_1')
  myimages.add('OrionBullets_FeO_5_4_0')
  myimages.add('OrionBullets_KCl')

  
  for myimagebase in myimages:
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.flux', outfile=myimagebase+'.image.pbcor', overwrite=True) # perform PBcorr
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits') # export the corrected image
    exportfits(imagename=myimagebase+'.flux', fitsimage=myimagebase+'.flux.fits') # export the PB image
