import PIL
from astropy.io import fits
from astropy import wcs
import pylab as pl
import pyavm
import regions

fn = "/Users/adam/Dropbox/2012_GeMS_OMC1/Trapezium_GEMS_mosaic_redblueorange_normed_large_contrast_bright_photoshop.png"
image = PIL.Image.open(fn)

wcsfn = '/Users/adam/Dropbox/2012_GeMS_OMC1/fullimage.wcs'
hdr = fits.Header.fromtextfile(wcsfn)
mywcs = wcs.WCS(hdr)

fig = pl.figure(1)
fig.clf()
ax = fig.add_subplot(111, projection=mywcs)
ax.imshow(image)

b4fov = regions.read_ds9('../regions/almab4fov.reg')[0]

b4patch = b4fov.to_pixel(mywcs).as_patch()
b4patch.set_facecolor('none')
b4patch.set_edgecolor('y')
ax.add_patch(b4patch)

regs = regions.read_ds9('../regions/bullet_apertures.reg')

for reg in regs:
    preg = reg.to_pixel(mywcs)
    patch = preg.as_patch()
    patch.set_facecolor('none')
    patch.set_edgecolor('white')
    ax.add_patch(patch)

ax.axis([4890, 8014, 7327, 10821])

lon = ax.coords['RA']
lat = ax.coords['Dec']
lon.set_axislabel('Right Ascension')
lat.set_axislabel('Declination')

lon.set_major_formatter('hh:mm:ss.s')
lat.set_major_formatter('dd:mm:ss.s')


fig.savefig("../figures/aperture_overlays.png", bbox_inches='tight', dpi=300)
