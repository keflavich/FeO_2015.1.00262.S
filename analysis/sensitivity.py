import paths
import radio_beam
from astropy.io import fits
from astropy import wcs
from astropy.stats import mad_std
from astropy import table
import regions
from latex_info import rounded, latexdict
from astropy import units as u


reg = regions.read_ds9(paths.rpath('centralcircle.reg'))[0]

fnames = {
    (3,-2): 'Band3_allspw_robust-2_continuum.image.tt0.pbcor.fits',
    (3,0): 'Band3_allspw_robust0_continuum.image.tt0.pbcor.fits',
    (3,2): 'Band3_allspw_robust2_continuum.image.tt0.pbcor.fits',
    (4,-2): 'Band4_allspw_robust-2_continuum.image.tt0.pbcor.fits',
    (4,0): 'Band4_allspw_robust0_continuum.image.tt0.pbcor.fits',
    (4,2): 'Band4_allspw_robust2_continuum.image.tt0.pbcor.fits',
}
freq = {4: 154*u.GHz,
        3: 101*u.GHz,}

measurements = []

for (band, robust), fn in fnames.items():
    fh = fits.open(paths.dpath(fn))

    preg = reg.to_pixel(wcs.WCS(fh[0].header))
    mask = preg.to_mask()

    data = mask.cutout(fh[0].data)[mask.data.astype('bool')]

    rms = mad_std(data)

    beam = radio_beam.Beam.from_fits_header(fh[0].header)
    jtok = beam.jtok(freq[band])

    measurements.append([band, robust, rounded(rms*1e3,rms*1e3)[0],
                         rounded(beam.major.to(u.arcsec), 0.1)[0],
                         rounded(beam.minor.to(u.arcsec), 0.1)[0],
                         rounded(beam.pa, 1.0)[0],
                         int(rounded(jtok.value, 100.0)[0]),
                        ])

tbl = table.Table(list(map(list, zip(*measurements))),
                  names=['Band', 'Robust', 'RMS', 'BMAJ', 'BMIN', 'BPA',
                         'K/Jy'])
tbl.sort('Robust')
tbl.sort('Band')
tbl['RMS'].unit = u.mJy

latexdict = latexdict.copy()
latexdict['header_start'] = '\label{tab:contsensitivity}'
tbl.write('../paper/rms_table.tex', format='ascii.latex', latexdict=latexdict)
