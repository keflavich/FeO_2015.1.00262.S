import copy
import glob
import os
from spectral_cube import SpectralCube
from spectral_cube.io import fits as scfits
from astropy.io import fits
from astropy import wcs

for fn in glob.glob("FITS/*.image.pbcor.fits"):
    print(fn)
    outfn = 'FITS/max/'+os.path.basename(fn.replace(".image.pbcor.fits","max.fits"))
    if os.path.exists(outfn):
        continue
    fh = fits.open(fn)
    #fh[0].header['ORIGIN'] = 'CASA 4.7.0-REL (r38335)'
    #print('Header origin: "{0}"'.format(fh[0].header['ORIGIN']))
    try:
        fh[0].header.tostring()
    except ValueError:
        fh[0].header.tostring()
    cube = scfits.load_fits_cube(fh)
    if hasattr(cube, 'I'):
        cube = cube.I
    print(cube)
    cube.beam_threshold=1
    print("Threshold set")
    mx = cube.max(axis=0)
    print("Max is done")
    print("mx header: ",mx.header['ORIGIN'])
    mx.write(outfn, overwrite=True)
