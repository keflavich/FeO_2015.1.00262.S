import numpy as np
from astropy.table import Table
from astropy import units as u
from astropy.io import ascii
import re
import paths

tbl = Table.read('lines.txt', format='ascii')

ok = tbl['band'] != 'None'

tbl = tbl[ok]


latexdict = ascii.latex.latexdicts['AA']
latexdict['tabletype'] = 'table*'
latexdict['tablealign'] = 'htp'
latexdict['units'] = {'Frequency':u.GHz.to_string(u.format.LatexInline)}
latexdict['header_start'] = '\label{tab:lines}'#\n\\footnotesize'

colnames = [('species','Species'),
            ('qn', 'Quantum Numbers'),
            ('freq', 'Frequency'),
            ('spw', 'SPW ID'),
           ]

for old, new in colnames:
    tbl.rename_column(old, new)


tbl['Quantum Numbers'] = np.array(
    ["\\ensuremath{{{0}}}".format(re.sub("\(([0-9,]+)\)", "_{\\1}", x))
     for x in tbl['Quantum Numbers']])

tbl.write(paths.tpath('lines_tbl.tex'), format='latex', latexdict=latexdict,
          overwrite=True)
