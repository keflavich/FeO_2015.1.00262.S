import glob
import pyspeckit
from astropy import units as u
import pylab as pl

for fn in glob.glob("*.fits"):
    sp = pyspeckit.Spectrum(fn)
    sp.xarr.convert_to_unit(u.GHz)
    sp.plotter(figure=pl.figure(1), clear=True)
    sp.plotter.savefig("pngs/{0}".format(fn.replace(".fits",".png")))
