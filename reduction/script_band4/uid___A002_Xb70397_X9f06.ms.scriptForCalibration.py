# ALMA Data Reduction Script

# Calibration

thesteps = []
step_title = {0: 'Import of the ASDM',
              1: 'Fix of SYSCAL table times',
              2: 'listobs',
              3: 'A priori flagging',
              4: 'Generation and time averaging of the WVR cal table',
              5: 'Generation of the Tsys cal table',
              6: 'Generation of the antenna position cal table',
              7: 'Application of the WVR, Tsys and antpos cal tables',
              8: 'Split out science SPWs and time average',
              9: 'Listobs, and save original flags',
              10: 'Initial flagging',
              11: 'Putting a model for the flux calibrator(s)',
              12: 'Save flags before bandpass cal',
              13: 'Bandpass calibration',
              14: 'Save flags before gain cal',
              15: 'Gain calibration',
              16: 'Save flags before applycal',
              17: 'Application of the bandpass and gain cal tables',
              18: 'Split out corrected column',
              19: 'Save flags after applycal'}

if 'applyonly' not in globals(): applyonly = False
try:
  print 'List of steps to be executed ...', mysteps
  thesteps = mysteps
except:
  print 'global variable mysteps not set.'
if (thesteps==[]):
  thesteps = range(0,len(step_title))
  print 'Executing all steps: ', thesteps

# The Python variable 'mysteps' will control which steps
# are executed when you start the script using
#   execfile('scriptForCalibration.py')
# e.g. setting
#   mysteps = [2,3,4]# before starting the script will make the script execute
# only steps 2, 3, and 4
# Setting mysteps = [] will make it execute all steps.

import re

import os

if applyonly != True: es = aU.stuffForScienceDataReduction()


#if re.search('^4.6.0', casadef.casa_version) == None:
# sys.exit('ERROR: PLEASE USE THE SAME VERSION OF CASA THAT YOU USED FOR GENERATING THE SCRIPT: 4.6.0')


# CALIBRATE_AMPLI:
# CALIBRATE_ATMOSPHERE: J0423-0120,J0541-0541,OrionBullets
# CALIBRATE_BANDPASS: J0423-0120
# CALIBRATE_FLUX: J0423-0120
# CALIBRATE_FOCUS:
# CALIBRATE_PHASE: J0541-0541
# CALIBRATE_POINTING: J0423-0120
# OBSERVE_CHECK:
# OBSERVE_TARGET: OrionBullets

# Using reference antenna = DV13

# Import of the ASDM
mystep = 0
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  if os.path.exists('uid___A002_Xb70397_X9f06.ms') == False:
    importasdm('uid___A002_Xb70397_X9f06', asis='Antenna Station Receiver Source CalAtmosphere CalWVR CorrelatorMode SBSummary', bdfflags=True, lazy=True, process_caldevice=False)
  if applyonly != True: es.fixForCSV2555('uid___A002_Xb70397_X9f06.ms')

# Fix of SYSCAL table times
mystep = 1
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  from recipes.almahelpers import fixsyscaltimes
  fixsyscaltimes(vis = 'uid___A002_Xb70397_X9f06.ms')

print "# A priori calibration"

# listobs
mystep = 2
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.listobs')
  listobs(vis = 'uid___A002_Xb70397_X9f06.ms',
    listfile = 'uid___A002_Xb70397_X9f06.ms.listobs')



# A priori flagging
mystep = 3
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms',
    mode = 'manual',
    spw = '5~12,17~24,29~46',
    autocorr = T,
    flagbackup = F)

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms',
    mode = 'manual',
    intent = '*POINTING*,*ATMOSPHERE*',
    flagbackup = F)

  flagcmd(vis = 'uid___A002_Xb70397_X9f06.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'plot',
    plotfile = 'uid___A002_Xb70397_X9f06.ms.flagcmd.png')

  flagcmd(vis = 'uid___A002_Xb70397_X9f06.ms',
    inpmode = 'table',
    useapplied = True,
    action = 'apply')


# Generation and time averaging of the WVR cal table
mystep = 4
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.wvr')

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.wvrgcal')

  # Warning: more than one integration time found on science data, I'm picking the lowest value. Please check this is right.

  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_Xb70397_X9f06.ms.wvrgcal')

  wvrgcal(vis = 'uid___A002_Xb70397_X9f06.ms',
    caltable = 'uid___A002_Xb70397_X9f06.ms.wvr',
    spw = [17, 19, 21, 23, 37, 39, 41, 43, 45],
    toffset = 0,
    tie = ['OrionBullets,J0541-0541'],
    statsource = 'OrionBullets')

  casalog.setlogfile(mylogfile)

  if applyonly != True: aU.plotWVRSolutions(caltable='uid___A002_Xb70397_X9f06.ms.wvr', spw='37', antenna='DV13',
    yrange=[-199,199],subplot=22, interactive=False,
    figfile='uid___A002_Xb70397_X9f06.ms.wvr.plots/uid___A002_Xb70397_X9f06.ms.wvr')

  #Note: If you see wraps in these plots, try changing yrange or unwrap=True
  #Note: If all plots look strange, it may be a bad WVR on the reference antenna.
  #      To check, you can set antenna='' to show all baselines.


# Generation of the Tsys cal table
mystep = 5
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.tsys')
  gencal(vis = 'uid___A002_Xb70397_X9f06.ms',
    caltable = 'uid___A002_Xb70397_X9f06.ms.tsys',
    caltype = 'tsys')

  # Flagging edge channels

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms.tsys',
    mode = 'manual',
    spw = '17:0~3;124~127,19:0~3;124~127,21:0~3;124~127,23:0~3;124~127,29:0~3;124~127,31:0~3;124~127,33:0~3;124~127,35:0~3;124~127',
    flagbackup = F)

  if applyonly != True: aU.plotbandpass(caltable='uid___A002_Xb70397_X9f06.ms.tsys', overlay='time',
    xaxis='freq', yaxis='amp', subplot=22, buildpdf=False, interactive=False,
    showatm=True,pwv='auto',chanrange='92.1875%',showfdm=True, showBasebandNumber=True, showimage=False,
    field='', figfile='uid___A002_Xb70397_X9f06.ms.tsys.plots.overlayTime/uid___A002_Xb70397_X9f06.ms.tsys')


  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.tsys', msName='uid___A002_Xb70397_X9f06.ms', interactive=False)


# Generation of the antenna position cal table
mystep = 6
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Position for antenna DV12 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV18 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA64 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA49 is derived from baseline run made on 2016-07-18 10:20:58.

  # Position for antenna DA62 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA60 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA45 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA44 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV17 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV16 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA63 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV25 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV09 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV11 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV19 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV10 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV22 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV13 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA52 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA53 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA50 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DA55 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV06 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV04 is derived from baseline run made on 2016-08-13 05:48:23.

  # Position for antenna DV05 is derived from baseline run made on 2016-08-13 05:48:23.

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.antpos')
  gencal(vis = 'uid___A002_Xb70397_X9f06.ms',
    caltable = 'uid___A002_Xb70397_X9f06.ms.antpos',
    caltype = 'antpos',
    antenna = 'DA44,DA45,DA49,DA50,DA52,DA53,DA55,DA60,DA62,DA63,DA64,DV04,DV05,DV06,DV09,DV10,DV11,DV12,DV13,DV16,DV17,DV18,DV19,DV22,DV25',
    #parameter = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
    parameter = [2.24370e-04,-4.85189e-04,-2.21192e-04,1.91216e-04,-4.09448e-04,-1.83005e-04,1.78725e-04,-3.84130e-04,-1.70005e-04,1.88096e-04,-3.91212e-04,-1.94924e-04,2.16199e-04,-5.44460e-04,-2.24561e-04,1.61656e-04,-3.82062e-04,-1.51282e-04,-9.99580e-05,4.47878e-04,1.77996e-04,-1.53881e-04,3.57768e-04,1.80659e-04,1.28174e-04,-3.23861e-04,-1.54633e-04,8.57720e-05,-2.83710e-04,-1.00700e-04,1.35606e-04,-2.89266e-04,-1.46677e-04,2.70989e-04,-8.89690e-04,-2.82455e-04,6.19354e-05,-1.83113e-04,-8.03721e-05,3.65306e-04,-1.06745e-03,-1.83559e-04,1.70374e-04,-1.99937e-04,-3.55030e-04,1.82355e-04,-4.14091e-04,-2.11617e-04,8.09519e-05,-1.47752e-04,-4.57172e-05,3.40780e-04,-4.79199e-04,-3.74174e-04,2.05904e-04,-5.58869e-04,-2.45907e-04,1.80529e-04,-3.99145e-04,-1.74038e-04,2.19224e-04,-4.80464e-04,-2.41299e-04,1.21017e-04,-3.80397e-04,-1.52805e-04,1.11453e-04,-3.33179e-04,-1.41488e-04,-1.96738e-05,-9.18982e-05,-1.29005e-06,8.49350e-05,-2.34021e-04,-1.33257e-04])


  # antenna x_offset y_offset z_offset total_offset baseline_date
  # DV06     3.65306e-04   -1.06745e-03   -1.83559e-04    1.14307e-03      2016-08-13 05:48:23
  # DV04     2.70989e-04   -8.89690e-04   -2.82455e-04    9.71990e-04      2016-08-13 05:48:23
  # DV12     3.40780e-04   -4.79199e-04   -3.74174e-04    6.96971e-04      2016-08-13 05:48:23
  # DV13     2.05904e-04   -5.58869e-04   -2.45907e-04    6.44362e-04      2016-08-13 05:48:23
  # DA52     2.16199e-04   -5.44460e-04   -2.24561e-04    6.27380e-04      2016-08-13 05:48:23
  # DV17     2.19224e-04   -4.80464e-04   -2.41299e-04    5.80629e-04      2016-08-13 05:48:23
  # DA44     2.24370e-04   -4.85189e-04   -2.21192e-04    5.78512e-04      2016-08-13 05:48:23
  # DV10     1.82355e-04   -4.14091e-04   -2.11617e-04    4.99506e-04      2016-08-13 05:48:23
  # DA55    -9.99580e-05    4.47878e-04    1.77996e-04    4.92208e-04      2016-08-13 05:48:23
  # DA45     1.91216e-04   -4.09448e-04   -1.83005e-04    4.87547e-04      2016-08-13 05:48:23
  # DA50     1.88096e-04   -3.91212e-04   -1.94924e-04    4.75838e-04      2016-08-13 05:48:23
  # DV16     1.80529e-04   -3.99145e-04   -1.74038e-04    4.71378e-04      2016-08-13 05:48:23
  # DA49     1.78725e-04   -3.84130e-04   -1.70005e-04    4.56508e-04      2016-07-18 10:20:58
  # DV09     1.70374e-04   -1.99937e-04   -3.55030e-04    4.41642e-04      2016-08-13 05:48:23
  # DA53     1.61656e-04   -3.82062e-04   -1.51282e-04    4.41577e-04      2016-08-13 05:48:23
  # DA60    -1.53881e-04    3.57768e-04    1.80659e-04    4.29319e-04      2016-08-13 05:48:23
  # DV18     1.21017e-04   -3.80397e-04   -1.52805e-04    4.27430e-04      2016-08-13 05:48:23
  # DA62     1.28174e-04   -3.23861e-04   -1.54633e-04    3.81085e-04      2016-08-13 05:48:23
  # DV19     1.11453e-04   -3.33179e-04   -1.41488e-04    3.78747e-04      2016-08-13 05:48:23
  # DA64     1.35606e-04   -2.89266e-04   -1.46677e-04    3.51537e-04      2016-08-13 05:48:23
  # DA63     8.57720e-05   -2.83710e-04   -1.00700e-04    3.13032e-04      2016-08-13 05:48:23
  # DV25     8.49350e-05   -2.34021e-04   -1.33257e-04    2.82377e-04      2016-08-13 05:48:23
  # DV05     6.19354e-05   -1.83113e-04   -8.03721e-05    2.09347e-04      2016-08-13 05:48:23
  # DV11     8.09519e-05   -1.47752e-04   -4.57172e-05    1.74568e-04      2016-08-13 05:48:23
  # DV22    -1.96738e-05   -9.18982e-05   -1.29005e-06    9.39894e-05      2016-08-13 05:48:23


# Application of the WVR, Tsys and antpos cal tables
mystep = 7
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]



  #from recipes.almahelpers import tsysspwmap
  #tsysmap = tsysspwmap(vis = 'uid___A002_Xb70397_X9f06.ms', tsystable = 'uid___A002_Xb70397_X9f06.ms.tsys', tsysChanTol = 1)

  tsysmap = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 23, 17, 17, 19, 19, 21, 21, 23, 23, 25, 26, 27, 28, 17, 17, 31, 32, 33, 34, 35, 23, 17, 17, 19, 19, 21, 21, 21,21, 23, 23]

  applycal(vis = 'uid___A002_Xb70397_X9f06.ms',
    field = '0',
    spw = '17,19,21,23,37,39,41,43,45',
    gaintable = ['uid___A002_Xb70397_X9f06.ms.tsys', 'uid___A002_Xb70397_X9f06.ms.wvr', 'uid___A002_Xb70397_X9f06.ms.antpos'],
    gainfield = ['0', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = T,
    flagbackup = F)

  tsysmap = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 17, 19, 21, 23, 17, 17, 19, 19, 21, 21, 23, 23, 25, 26, 27, 28, 17, 17, 31, 32, 33, 34, 35, 23, 17, 17, 19, 19, 21, 21, 21,21, 23, 23]

  applycal(vis = 'uid___A002_Xb70397_X9f06.ms',
    field = '1',
    spw = '17,19,21,23,37,39,41,43,45',
    gaintable = ['uid___A002_Xb70397_X9f06.ms.tsys', 'uid___A002_Xb70397_X9f06.ms.wvr', 'uid___A002_Xb70397_X9f06.ms.antpos'],
    gainfield = ['1', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = T,
    flagbackup = F)

  tsysmap = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 29, 29, 19, 20, 21, 22, 23, 35, 29, 31, 33, 35, 29, 29, 31, 31, 33, 33, 35, 35, 29, 29, 31, 31, 33, 33, 33,33,35, 35]

  applycal(vis = 'uid___A002_Xb70397_X9f06.ms',
    field = '2',
    spw = '17,19,21,23,37,39,41,43,45',
    gaintable = ['uid___A002_Xb70397_X9f06.ms.tsys', 'uid___A002_Xb70397_X9f06.ms.wvr', 'uid___A002_Xb70397_X9f06.ms.antpos'],
    gainfield = ['2', '', ''],
    interp = 'linear,linear',
    spwmap = [tsysmap,[],[]],
    calwt = T,
    flagbackup = F)



  if applyonly != True: es.getCalWeightStats('uid___A002_Xb70397_X9f06.ms')


# Split out science SPWs and time average
mystep = 8
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split')
  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.flagversions')

  split(vis = 'uid___A002_Xb70397_X9f06.ms',
    outputvis = 'uid___A002_Xb70397_X9f06.ms.split',
    datacolumn = 'corrected',
    spw = '17,19,21,23,37,39,41,43,45',
    keepflags = T)



print "# Calibration"

# Listobs, and save original flags
mystep = 9
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.listobs')
  listobs(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    listfile = 'uid___A002_Xb70397_X9f06.ms.split.listobs')


  if not os.path.exists('uid___A002_Xb70397_X9f06.ms.split.flagversions/Original.flags'):
    flagmanager(vis = 'uid___A002_Xb70397_X9f06.ms.split',
      mode = 'save',
      versionname = 'Original')



# Initial flagging
mystep = 10
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  # Flagging shadowed data

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'shadow',
    flagbackup = F)

  # Flagging edge channels

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'manual',
    spw = '0:0~7;120~127,1:0~7;120~127,2:0~7;120~127,3:0~7;120~127',
    flagbackup = F)

  # Flagging outliers in phase vs uvdist plots

  flagdata(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'manual',
    antenna='DA59,DV19',
    flagbackup = F)



# Putting a model for the flux calibrator(s)
mystep = 11
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  setjy(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    standard = 'manual',
    field = 'J0423-0120',
    fluxdensity = [0.711532116662, 0, 0, 0],
    spix = -0.771355199809,
    reffreq = '154.656059726GHz')



# Save flags before bandpass cal
mystep = 12
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  flagmanager(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'save',
    versionname = 'BeforeBandpassCalibration')



# Bandpass calibration
mystep = 13
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.ap_pre_bandpass')

  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.ap_pre_bandpass',
    field = '0', # J0423-0120
    spw = '0:0~128,1:0~128,2:0~128,3:0~128,4:0~3840,5:0~1920,6:0~1920,7:0~3840,8:0~3840',
    scan = '1,3,5',
    solint = 'int',
    refant = 'DV13',
    calmode = 'p')

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.ap_pre_bandpass', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.bandpass')
  bandpass(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.bandpass',
    field = '0', # J0423-0120
    scan = '1,3,5',
    solint = 'inf',
    combine = 'scan',
    refant = 'DV13',
    solnorm = False,
    bandtype = 'B',
    gaintable = 'uid___A002_Xb70397_X9f06.ms.split.ap_pre_bandpass')

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.bandpass', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)


  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phasediff_inf')
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf',
    field = '0',
    solint = 'inf',
    refant = 'DV13',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_Xb70397_X9f06.ms.split.bandpass')

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phase_int')
  #for i in [0, 1]: # J0423-0120,J0541-0541
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
      caltable = 'uid___A002_Xb70397_X9f06.ms.split.phase_int',
      field = '0,1',
      solint = 'int',
      combine = 'spw',
      refant = 'DV13',
      gaintype = 'G',
      calmode = 'p',
      #append = True,
      gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf'])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phase_int', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  calspwmap = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.ampli_inf')
  #for i in [0, 1]: # J0423-0120,J0541-0541
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
      caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf',
      field = "0,1",
      solint = 'inf',
      combine = 'spw',
      refant = 'DV13',
      gaintype = 'T',
      calmode = 'a',
      #append = True,
      gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', 'uid___A002_Xb70397_X9f06.ms.split.phase_int'],
      spwmap = [[],[],[0, 0, 0, 0, 0, 0, 0, 0, 0]])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.ampli_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.flux_inf')
  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.fluxscale')
  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_Xb70397_X9f06.ms.split.fluxscale')

  fluxscaleDict = fluxscale(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf',
    fluxtable = 'uid___A002_Xb70397_X9f06.ms.split.flux_inf',
    reference = '0', # J0423-0120
    refspwmap = calspwmap[0],
    incremental = True)

  casalog.setlogfile(mylogfile)

  if applyonly != True: es.fluxscale2(caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf', removeOutliers=True, msName='uid___A002_Xb70397_X9f06.ms', writeToFile=True, preavg=10000)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phase_inf')
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.phase_inf',
    field = '0~1', # J0423-0120,J0541-0541
    solint = 'inf',
    combine = 'spw',
    refant = 'DV13',
    gaintype = 'G',
    calmode = 'p',
    gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf'])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phase_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  setjy(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    standard = 'manual',
    field = 'J0423-0120',
    fluxdensity = [0.711532116662, 0, 0, 0],
    spix = -0.771355199809,
    reffreq = '154.656059726GHz')

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.bandpass2')
  bandpass(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.bandpass2',
    field = '0', # J0423-0120
    scan = '1,3,5',
    solint = 'inf,20MHz',
    combine = 'scan',
    refant = 'DV13',
    solnorm = False,
    bandtype = 'B',
    gaintable = 'uid___A002_Xb70397_X9f06.ms.split.ap_pre_bandpass')

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.bandpass2', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)


# Save flags before gain cal
mystep = 14
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  flagmanager(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'save',
    versionname = 'BeforeGainCalibration')



# Gain calibration
mystep = 15
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phasediff_inf')
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf',
    field = '0',
    solint = 'inf',
    refant = 'DV13',
    gaintype = 'G',
    calmode = 'p',
    gaintable = 'uid___A002_Xb70397_X9f06.ms.split.bandpass2')

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phase_int')
  #for i in [0, 1]: # J0423-0120,J0541-0541
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
      caltable = 'uid___A002_Xb70397_X9f06.ms.split.phase_int',
      field = '0,1',
      solint = 'int',
      combine = 'spw',
      refant = 'DV13',
      gaintype = 'G',
      calmode = 'p',
      #append = True,
      gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass2', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf'])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phase_int', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  calspwmap = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.ampli_inf')
  #for i in [0, 1]: # J0423-0120,J0541-0541
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
      caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf',
      field = '0,1',
      solint = 'inf',
      combine = 'spw',
      refant = 'DV13',
      gaintype = 'T',
      calmode = 'a',
      #append = True,
      gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass2', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', 'uid___A002_Xb70397_X9f06.ms.split.phase_int'],
      spwmap = [[],[],[0, 0, 0, 0, 0, 0, 0, 0, 0]])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.ampli_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.flux_inf')
  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.fluxscale')
  mylogfile = casalog.logfile()
  casalog.setlogfile('uid___A002_Xb70397_X9f06.ms.split.fluxscale')

  fluxscaleDict = fluxscale(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf',
    fluxtable = 'uid___A002_Xb70397_X9f06.ms.split.flux_inf',
    reference = '0', # J0423-0120
    refspwmap = calspwmap[0],
    incremental = True)

  casalog.setlogfile(mylogfile)

  if applyonly != True: es.fluxscale2(caltable = 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf', removeOutliers=True, msName='uid___A002_Xb70397_X9f06.ms', writeToFile=True, preavg=10000)

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.phase_inf')
  gaincal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    caltable = 'uid___A002_Xb70397_X9f06.ms.split.phase_inf',
    field = '0~1', # J0423-0120,J0541-0541
    solint = 'inf',
    combine = 'spw',
    refant = 'DV13',
    gaintype = 'G',
    calmode = 'p',
    gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass2', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf'])

  if applyonly != True: es.checkCalTable('uid___A002_Xb70397_X9f06.ms.split.phase_inf', msName='uid___A002_Xb70397_X9f06.ms.split', interactive=False)


# Save flags before applycal
mystep = 16
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  flagmanager(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    mode = 'save',
    versionname = 'BeforeApplycal')



# Application of the bandpass and gain cal tables
mystep = 17
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  calspwmap = {0: [0, 0, 0, 0, 0, 0, 0, 0, 0], 1: [0, 0, 0, 0, 0, 0, 0, 0, 0]}

  applycal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    field = '0', # J0423-0120
    gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass2', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', 'uid___A002_Xb70397_X9f06.ms.split.phase_int'],
    gainfield = ['0', '0', '0'],
    interp = [],
    spwmap = [[], [], calspwmap[0]],
    calwt = T,
    flagbackup = F)


  applycal(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    field = '1,2', # OrionBullets
    gaintable = ['uid___A002_Xb70397_X9f06.ms.split.bandpass2', 'uid___A002_Xb70397_X9f06.ms.split.phasediff_inf', 'uid___A002_Xb70397_X9f06.ms.split.phase_inf', 'uid___A002_Xb70397_X9f06.ms.split.ampli_inf', 'uid___A002_Xb70397_X9f06.ms.split.flux_inf'],
    gainfield = ['', '', '1', '1', '1'], # J0541-0541
    interp = ['', 'nearest', 'linearPD', '', ''],
    spwmap = [[], [], calspwmap[1], calspwmap[1], calspwmap[1]],
    calwt = T,
    flagbackup = F)


# Split out corrected column
mystep = 18
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]

  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.cal')
  os.system('rm -rf uid___A002_Xb70397_X9f06.ms.split.cal.flagversions')

  listOfIntents = ['CALIBRATE_BANDPASS#ON_SOURCE',
   'CALIBRATE_FLUX#ON_SOURCE',
   'CALIBRATE_PHASE#ON_SOURCE',
   'CALIBRATE_WVR#AMBIENT',
   'CALIBRATE_WVR#HOT',
   'CALIBRATE_WVR#OFF_SOURCE',
   'CALIBRATE_WVR#ON_SOURCE',
   'OBSERVE_TARGET#ON_SOURCE']

  split(vis = 'uid___A002_Xb70397_X9f06.ms.split',
    outputvis = 'uid___A002_Xb70397_X9f06.ms.split.cal',
    datacolumn = 'corrected',
    intent = ','.join(listOfIntents),
    keepflags = T)



# Save flags after applycal
mystep = 19
if(mystep in thesteps):
  casalog.post('Step '+str(mystep)+' '+step_title[mystep],'INFO')
  print 'Step ', mystep, step_title[mystep]


  flagmanager(vis = 'uid___A002_Xb70397_X9f06.ms.split.cal',
    mode = 'save',
    versionname = 'AfterApplycal')
