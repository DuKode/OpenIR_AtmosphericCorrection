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
    print("""
openir_atmosphericcorrection.py TO DO """)
    sys.exit(1)
