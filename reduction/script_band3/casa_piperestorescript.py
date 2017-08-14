__rethrow_casa_exceptions = True
h_init()
try:
    hif_restoredata (vis=['uid___A002_Xb62a5b_X6aa4', 'uid___A002_Xb62a5b_X6ffc', 'uid___A002_Xc02418_X6d20'], session=['session_1', 'session_1', 'session_2'], ocorr_mode='ca')
finally:
    h_save()
