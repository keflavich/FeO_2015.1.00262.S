vis='uid___A002_Xb70397_X9f06.ms.split.cal'

for spwnum in range(4,9):
    for robust in (-2, 0, 2):
        output = "Band4_spw{0}_robust{1}_cube".format(spwnum, robust)
        os.system('rm -rf ' + output + '*/')
        tclean(vis=vis,
               imagename=output,
               field='OrionBullets',
               spw='{0}'.format(spwnum),
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

        output = "Band4_spw{0}_robust{1}_continuum".format(spwnum, robust)
        os.system('rm -rf ' + output + '*/')
        tclean(vis=vis,
               imagename=output,
               field='OrionBullets',
               spw='{0}'.format(spwnum),
               gridder='standard',
               specmode='mfs',
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

for robust in (-2, 0, 2):
    output = "Band4_allspw_robust{0}_continuum".format(robust)
    os.system('rm -rf ' + output + '*/')
    tclean(vis=vis,
           imagename=output,
           field='OrionBullets',
           spw='',
           gridder='standard',
           specmode='mfs',
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
