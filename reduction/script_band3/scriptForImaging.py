#==================================================
# CONCAT

concat(vis = ['uid___A002_Xb62a5b_X6aa4.ms','uid___A002_Xb62a5b_X6ffc.ms','uid___A002_Xc02418_X6d20.ms'],
       concatvis = 'calibrated.ms')

listobs( vis = 'calibrated.ms',
         listfile = 'calibrated.ms.listobs')

#==================================================
clean(vis = 'calibrated.ms',
      imagename = 'OrionBullets_spw25',
      field = 'OrionBullets', # TARGET 
      spw = '25,82,100',
      imagermode = 'csclean',
      mode = 'frequency',
      width = '244.141kHz', 
      nchan = -1,
      start = '',
      interpolation = 'linear',
      outframe = 'LSRK', 
      niter = 1000,
      interactive = T,
      npercycle = 100,
      imsize = [1200,1200],
      cell = '0.087arcsec',
      restfreq = '94.05GHz',
      weighting = 'briggs',
      robust = -0.5)


#Create fits datacubes for science targets
exportfits(imagename='OrionBullets_spw25.image', fitsimage='OrionBullets_spw25.fits')
exportfits(imagename='OrionBullets_spw25.flux', fitsimage='OrionBullets_spw25.flux.fits')

#Generate beam corrected images
immath(imagename = ['OrionBullets_spw25.fits', 'OrionBullets_spw25.flux.fits'],
       mode = 'evalexpr', expr = 'IM0/IM1', outfile = 'OrionBullets_spw25.pbcorr')

exportfits(imagename='OrionBullets_spw25.pbcorr', fitsimage='OrionBullets_spw25.pbcorr.fits')

