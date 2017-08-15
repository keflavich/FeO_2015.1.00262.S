#!/bin/sh

#This script is ment to be set in the COMMAND variable
#in the configure file to submit.  That submit script will create the
#clusterspec file for us in the WORK_DIR we specified in the configure file.

WORK_DIR='/lustre/aginsbur/orion/2015.1.00262.S/science_goal.uid___A001_X2fe_X953/group.uid___A001_X2fe_X954/member.uid___A001_X2fe_X955/calibrated'
cd ${WORK_DIR}

# casa's python requires a DISPLAY for matplot so create a virtual X server
xvfb-run -d casa --nogui -c scriptForImaging_spws.py
#-c "field_list=['W51 North']; execfile('$WORK_DIR/imaging_continuum_selfcal.py')"
