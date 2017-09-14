import numpy as np
from spectral_cube import SpectralCube
from astropy import units as u
from astropy import table
import paths

lines = table.Table.read(('/lustre/aginsbur/orion/2015.1.00262.S/analysis/lines.txt'), format='ascii')
linenames = ["{0} {1}".format(x,y) for x,y in zip(lines['species'], lines['qn'])]


for ii,line in enumerate(lines):

    #if line['diffuse'] == 'n':
    #    continue

    band = int(line['band']) if line['band'] != 'None' else None
    if band is None:
        continue
    spw = int(line['spw'])

    if band==4:
        spw = int((spw - 37)/2) + 4

    fn = ('Band{band}_spw{spw}_robust2_cube.image.pbcor.fits'
          .format(spw=spw, band=band))

    cube = SpectralCube.read(fn)
    vcube = cube.with_spectral_unit(u.km/u.s,
                                    velocity_convention='radio',
                                    rest_value=line['freq']*u.GHz)
                                
    vslab = vcube.spectral_slab(5*u.km/u.s, 13*u.km/u.s).minimal_subcube()
    kvslab = vslab.to(u.K)

    mom0 = kvslab.moment0(axis=0)
    mx = kvslab.max(axis=0)
    mom0.write('moments/{0}_moment0.fits'.format(line['species_txt']), overwrite=True)
    mx.write('moments/{0}_max.fits'.format(line['species_txt']), overwrite=True)
