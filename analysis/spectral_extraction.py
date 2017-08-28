import os
import glob
from astropy import log
from astropy import units as u
import numpy as np
from spectral_cube import SpectralCube
import pyregion
import radio_beam
import socket

if 'nmpost' in socket.gethostname():
    dpath = lambda x: os.path.join("/lustre/aginsbur/orion/2015.1.00262.S/FITS",x)
    rpath = lambda x: os.path.join("/lustre/aginsbur/orion/2015.1.00262.S/regions",x)
    spath = lambda x: os.path.join("/lustre/aginsbur/orion/2015.1.00262.S/FITS/spectra",x)
else:
    raise ValueError("No match to socket hostname {0}.".format(socket.gethostname()))


regions = (
           pyregion.open(rpath('contsource_locations.reg'))+
           pyregion.open(rpath('bullet_apertures.reg'))
          )

for cubename in glob.glob(dpath("*.image.pbcor.fits")):
    print(cubename)

    try:
        cube = SpectralCube.read(dpath(cubename)).mask_out_bad_beams(threshold=0.1)
    except Exception as ex:
        print("Skipping {0} because {1}".format(cubename, ex))
        continue
    print(cube)

    stdfpath = spath(cubename.replace(".image.pbcor.fits","_std.fits"))
    if not os.path.exists(stdfpath):
        stddev = cube.std(axis=(1,2))
        stddev.write(stdfpath)

    for reg in regions:

        name = reg.attr[1]['text']
        fname = name.replace(" ","_").lower()

        suffix = os.path.split(os.path.splitext(cubename)[0])[1]
        if os.path.exists(spath("{1}_{0}.fits".format(suffix,fname))):
            print("Skipping {0} {1} because it exists".format(suffix, fname))
            continue

        CL = reg.coord_list
        if reg.name == 'circle':
            radius = CL[2]
            reg = pyregion.ShapeList([reg])
            bgSL = pyregion.parse("fk5; circle({0},{1},{2}\")"
                                  .format(CL[0],
                                          CL[1],
                                          2*radius*3600))
        elif reg.name == 'ellipse':
            reg = pyregion.ShapeList([reg])
            bgSL = pyregion.parse("fk5; circle({0},{1},{2}\")"
                                  .format(CL[0],
                                          CL[1],
                                          2*CL[2]*3600,
                                          2*CL[3]*3600))
        else:
            radius = 0.5
            reg = pyregion.parse("fk5; circle({0},{1},0.5\")"
                                 .format(CL[0], CL[1]))
            bgSL = pyregion.parse("fk5; circle({0},{1},{2}\")"
                                  .format(CL[0],
                                          CL[1],
                                          2*radius))

        try:
            scube = cube.subcube_from_ds9region(reg)
            if scube.size == 0:
                print("Skipping {0} because it is empty.".format(name))
                continue
        except ValueError as ex:
            print("Skipping {0} because {1}".format(name, ex))
            continue

        log.info("Source name: {0}  filename: {1}".format(name,fname))
        print(scube)
        spsum = scube.sum(axis=(1,2))
        assert np.any(np.isfinite(spsum))
        spnpix = np.count_nonzero(np.isfinite(scube[300,:,:]))
        assert spnpix > 0
        spectrum = spsum / spnpix
        # I think this is a hack left over from old versions of SpectralCube
        spsum.meta['beam'] = radio_beam.Beam(major=np.nanmedian([bm.major.to(u.deg).value for bm in scube.beams]),
                                             minor=np.nanmedian([bm.minor.to(u.deg).value for bm in scube.beams]),
                                             pa=np.nanmedian([bm.pa.to(u.deg).value for bm in scube.beams]),)

        hdu = spsum.hdu
        hdu.data = spectrum.value
        pixel_scale = np.abs(cube.wcs.celestial.pixel_scale_matrix.diagonal().prod())**0.5 * u.deg
        hdu.header['PPBEAM'] = (spsum.meta['beam'].sr / pixel_scale**2).decompose().value

        hdu.header['OBJECT'] = name

        hdu.writeto(spath("{1}_{0}.fits".format(suffix,fname,)),
                    overwrite=True)
        print(spath("{1}_{0}.fits".format(suffix, fname, )))

        bgsc = cube.subcube_from_ds9region(bgSL)
        print(bgsc)
        npix = np.count_nonzero(np.isfinite(bgsc[1000,:,:]))
        assert npix > 0
        bgsum = bgsc.sum(axis=(1,2))
        assert np.any(np.isfinite(bgsum))
        bgspec = (bgsum - spsum) / npix
        bgspec.meta['beam'] = radio_beam.Beam(major=np.nanmedian([bm.major.to(u.deg).value for bm in scube.beams]),
                                              minor=np.nanmedian([bm.minor.to(u.deg).value for bm in scube.beams]),
                                              pa=np.nanmedian([bm.pa.to(u.deg).value for bm in scube.beams]),
                                             )
        bghdu = bgspec.hdu
        bghdu.header['OBJECT'] = name
        bghdu.writeto(spath("{0}_background_mean{1}.fits".format(fname,
                                                                 suffix)),
                      overwrite=True)
