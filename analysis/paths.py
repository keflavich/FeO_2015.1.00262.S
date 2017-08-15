import os

root = os.path.expanduser('~/work/feo/')

datapath = os.path.join(root, 'FITS/')
texpath = os.path.join(root, 'tex/')
figurepath = os.path.join(root, 'figures/')
regpath = os.path.join(root, 'regions/')
analysispath = os.path.join(root, 'analysis/')
plotcodepath = os.path.join(root, 'plot_codes/')
observingpath = os.path.join(root, 'observing/')
tablepath = os.path.join(root, 'tables/')
spectrum_path = os.path.join(root, 'FITS/12m/spectra')
merge_spectrum_path = os.path.join(root, 'FITS/merge/spectra')

def path(x, basepath):
    return os.path.join(basepath, x)

def fpath(x, figurepath=figurepath):
    return os.path.join(figurepath, x)

def rpath(x, regpath=regpath):
    return os.path.join(regpath, x)

def opath(x, observingpath=observingpath):
    return os.path.join(observingpath, x)

def pcpath(x, plotcodepath=plotcodepath):
    return os.path.join(plotcodepath, x)

def apath(x, analysispath=analysispath):
    return os.path.join(analysispath, x)

def dpath(x, datapath=datapath):
    return os.path.join(datapath, x)

def dpath12m(x, datapath=datapath):
    return os.path.join(datapath, '12m', x)

def dpathmerge(x, datapath=datapath):
    return os.path.join(datapath, 'merge', x)

def dppath(x, datapath=datapath):
    return os.path.join(datapath, 'projections', x)

def tpath(x, tablepath=tablepath):
    return os.path.join(tablepath, x)

def texpath(x, texpath=texpath):
    return os.path.join(texpath, x)

def spath(x, spectrum_path=spectrum_path):
    return os.path.join(spectrum_path, x)

def merge_spath(x, spectrum_path=merge_spectrum_path):
    return os.path.join(spectrum_path, x)
