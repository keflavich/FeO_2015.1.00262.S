import numpy as np
import pylab as pl
from astropy import wcs
from astropy.io import fits
from spectral_cube import SpectralCube
from astropy import units as u
from astropy import table
import paths

lines = table.Table.read(paths.apath('lines.txt'), format='ascii')
linenames = ["{0} {1}".format(x,y) for x,y in zip(lines['species'], lines['qn'])]


for ii,line in enumerate(lines):

    if line['diffuse'] == 'n':
        continue

    band = int(line['band']) if line['band'] != 'None' else None
    if band is None:
        continue
    spw = int(line['spw'])

    mom0 = fits.open(paths.dpath('moments/{0}_moment0.fits'.format(line['species_txt'])))
    mx = fits.open(paths.dpath('moments/{0}_max.fits'.format(line['species_txt'])))

    mywcs = wcs.WCS(mx[0].header)

    fig = pl.figure(1)
    fig.clf()
    ax = fig.add_subplot(111, projection=mywcs)
    im = ax.imshow(mom0[0].data, cmap='gray_r', interpolation='nearest', origin='lower',)

    lon = ax.coords['RA']
    lat = ax.coords['Dec']
    lon.set_axislabel('Right Ascension')
    lat.set_axislabel('Declination')

    lon.set_major_formatter('hh:mm:ss.s')
    lat.set_major_formatter('dd:mm:ss.s')

    pl.colorbar(mappable=im)

    fig.savefig(paths.fpath('{0}_moment0.png'.format(line['species_txt'])))

    fig.clf()
    ax = fig.add_subplot(111, projection=mywcs)
    im = ax.imshow(mx[0].data, cmap='gray_r', interpolation='nearest', origin='lower')

    lon = ax.coords['RA']
    lat = ax.coords['Dec']
    lon.set_axislabel('Right Ascension')
    lat.set_axislabel('Declination')

    lon.set_major_formatter('hh:mm:ss.s')
    lat.set_major_formatter('dd:mm:ss.s')

    pl.colorbar(mappable=im)

    fig.savefig(paths.fpath('{0}_max.png'.format(line['species_txt'])))
