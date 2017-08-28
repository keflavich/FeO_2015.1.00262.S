import os
import glob
import pyspeckit
from astropy import units as u
import pylab as pl
from astropy import table
import paths

lines = table.Table.read(paths.apath('lines.txt'), format='ascii')
linenames = ["{0} {1}".format(x,y) for x,y in zip(lines['species'], lines['qn'])]


for fn in glob.glob(paths.spath("*.fits")):
    sp = pyspeckit.Spectrum(fn)
    sp.xarr.convert_to_unit(u.GHz)
    sp.plotter(figure=pl.figure(1), clear=True)
    sp.plotter.line_ids(linenames, lines['freq']*u.GHz, plot_kwargs={'color':'r'},
                        velocity_offset=9*u.km/u.s)
    sp.plotter.savefig(paths.spath("pngs/{0}".format(os.path.split(fn)[-1].replace(".fits",".png"))))
