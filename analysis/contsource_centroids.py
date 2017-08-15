from paths import rpath, tpath, fpath
import regions
from gaussfit_catalog import gaussfit_catalog, gaussfit_image
from astropy.table import Table, Column
from astropy import coordinates, units as u

def data_to_table(fit_data):
    names = fit_data.keys()
    numnames = names
    stripnames = names
    stripnames = [fullname for nnm,fullname in sorted(zip(numnames,stripnames))]
    names = [fullname for nnm,fullname in sorted(zip(numnames,names))]
    namecol = Column(name='Name', data=stripnames)
    colnames = ['amplitude', 'center_x', 'center_y', 'fwhm_major', 'fwhm_minor', 'pa',
                'chi2', 'chi2/n', 'e_amplitude', 'e_center_x', 'e_center_y',
                'e_fwhm_major', 'e_fwhm_minor', 'e_pa', 'success',]
    columns = [Column(name=k, data=[fit_data[entry][k].value
                                    if hasattr(fit_data[entry][k],'value')
                                    else fit_data[entry][k]
                                    for entry in names],
                      unit=(fit_data[names[0]][k].unit
                            if hasattr(fit_data[names[0]][k], 'unit')
                            else None))
               for k in colnames]

    return Table([namecol]+columns)

if __name__ == "__main__":
    regs = regions.read_ds9(rpath('contsource_approxlocations.reg'))

    from files import band4cont

    fit_data = gaussfit_catalog(band4cont, regs, savepath=fpath('gaussfits'))

    tbl = data_to_table(fit_data)

    tbl.rename_column("chi2/n", "chi2_n")
    tbl.write(tpath("gaussian_fit_table.ipac"), format='ascii.ipac',
              overwrite=True)

    with open(rpath('contsource_locations.reg'),'w') as fh:
        fh.write("fk5\n")
        for reg in regs:
            ii = reg.meta['text'].strip("{}")
            crd = coordinates.SkyCoord(fit_data[str(ii)]['center_x'],
                                       fit_data[str(ii)]['center_y'], frame='fk5')
            fh.write("point({0}, {1}) # point=x text={{source{2}}}\n"
                     .format(crd.ra.to_string(u.hour, sep=":"),
                             crd.dec.to_string(sep=":"), ii))
