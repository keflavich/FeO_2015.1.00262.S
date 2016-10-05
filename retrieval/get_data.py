from astroquery.alma import Alma

alma = Alma()
alma.login('keflavich')
alma.cache_location = '.'

rslt = alma.query(payload={'project_code':'2015.1.00262.S'}, public=False)

data = alma.retrieve_data_from_uid(rslt['Member ous id'])
#data = alma.retrieve_data_from_uid(rslt['Asdm uid'])
