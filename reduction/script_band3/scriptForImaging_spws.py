vis = ['uid___A002_Xb62a5b_X6aa4.ms','uid___A002_Xb62a5b_X6ffc.ms','uid___A002_Xc02418_X6d20.ms']
spw_ids = [['25','25','25'],
           ['27','27','27'],
           ['29','29','29'],
           ['31','31','31'],
           ['33','33','33'],
           ['35','35','35'],
          ]

for spwnum in spw_ids:
    for robust in (-2, 0, 2):
        output = "Band3_spw{0}_robust{1}_cube".format(spwnum[0], robust)
        os.system('rm -rf ' + output + '*/')
        tclean(vis=vis,
               imagename=output,
               field='OrionBullets',
               spw=spwnum,
               gridder='standard',
               specmode='cube',
               veltype='radio',
               outframe='LSRK',
               interactive=False,
               niter=1000,
               imsize=[640,640],
               cell='0.1arcsec',
               weighting='briggs',
               robust=robust,
               phasecenter='',
               threshold='10mJy',
               savemodel='none',
              )
        myimagebase = output
        impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
        exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
        exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
        exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)
        for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                       'image', 'residual'):
            os.system('rm -rf {0}.{1}'.format(output, suffix))

        output = "Band3_spw{0}_robust{1}_continuum".format(spwnum, robust)
        os.system('rm -rf ' + output + '*/')
        tclean(vis=vis,
               imagename=output,
               field='OrionBullets',
               spw=spwnum,
               gridder='standard',
               specmode='mtmfs',
               veltype='radio',
               outframe='LSRK',
               interactive=False,
               niter=1000,
               imsize=[640,640],
               cell='0.1arcsec',
               weighting='briggs',
               robust=robust,
               phasecenter='',
               nterms=2,
               threshold='10mJy',
               savemodel='none',
              )
        myimagebase = output
        impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
        exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
        exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
        exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)
        for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                       'image', 'residual'):
            os.system('rm -rf {0}.{1}'.format(output, suffix))

allspw = [",".join(x) for x in (zip(*spw_ids))]
for robust in (-2, 0, 2):
    output = "Band3_allspw_robust{0}_continuum".format(robust)
    os.system('rm -rf ' + output + '*/')
    tclean(vis=vis,
           imagename=output,
           field='OrionBullets',
           spw=allspw,
           gridder='standard',
           specmode='mtmfs',
           nterms=2,
           veltype='radio',
           outframe='LSRK',
           interactive=False,
           niter=1000,
           imsize=[640,640],
           cell='0.1arcsec',
           weighting='briggs',
           robust=robust,
           phasecenter='',
           threshold='10mJy',
           savemodel='none',
          )
    myimagebase = output
    impbcor(imagename=myimagebase+'.image', pbimage=myimagebase+'.pb', outfile=myimagebase+'.image.pbcor', overwrite=True)
    exportfits(imagename=myimagebase+'.image.pbcor', fitsimage=myimagebase+'.image.pbcor.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.pb', fitsimage=myimagebase+'.pb.fits', overwrite=True, dropdeg=True)
    exportfits(imagename=myimagebase+'.residual', fitsimage=myimagebase+'.residual.fits', overwrite=True, dropdeg=True)
    for suffix in ('pb', 'weight', 'sumwt', 'psf', 'model', 'mask',
                   'image', 'residual'):
        os.system('rm -rf {0}.{1}'.format(output, suffix))
