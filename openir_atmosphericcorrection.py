#!/usr/bin/env python2.7
#******************************************************************************
#  Name:     openir_atmosphericcorrection
#  Project:  OpenIR - GDAL Python Interface
#  Purpose:  atmospheric correction 
#  Author:   dukodestudio, team@dukodestudio.com
# 
#******************************************************************************
# the dukode studio 
# http://dukodestudio.com
#******************************************************************************

try:
    from osgeo import gdal
except ImportError:
    import gdal

import sys
import os.path

def Usage():
    print(""" openir_atmosphericcorrection.py [sourcefile] [dstfile] """)
    sys.exit(1)

# =============================================================================
# 	Mainline
# =============================================================================

quiet_flag = 0
src_filename = None
src_band = 1

dst_filename = None
format = 'GTiff'
creation_options = []

argv = gdal.GeneralCmdLineProcessor( sys.argv )
argv = gdal.GeneralCmdLineProcessor( sys.argv )
if argv is None:
    sys.exit( 0 )

print "x"
# ############################
# Parse command line arguments.
# ############################
i = 1
while i < len(argv):
    arg = argv[i]

    if arg[:2] == '-h':
        Usage()

    elif src_filename is None:
        src_filename = argv[i]

    elif dst_filename is None:
        dst_filename = argv[i]

    else:
        Usage()

    i = i + 1

if src_filename is None:
    Usage()


print "SOURCE FILE "+ src_filename
print "DESTINATION FILE "+ dst_filename
# ###################################################
# DETERMINE THE BAND. 
# ###################################################





#
# PROCESS TILE
#