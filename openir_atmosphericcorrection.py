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
from gdalconst import *

def Usage():
    print("""USAGE: openir_atmosphericcorrection.py [sourcefile] [dstfile] """)
    sys.exit(1)

# =============================================================================
# 	Mainline
# =============================================================================

quiet_flag = 0
src_filename = None
src_band = None

dst_filename = None
format = 'GTiff'
creation_options = []

gdal.AllRegister() #what is that for? 
argv = gdal.GeneralCmdLineProcessor( sys.argv )
if argv is None:
    sys.exit( 0 )

# print "x"
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

if dst_filename is None:
    Usage()


# ###################################################
# DETERMINE THE BAND. read geotiff metadata 
# ###################################################


# #############################################################################
# PROCESS TILE
# #############################################################################
# =============================================================================
#	Setup Atmospheric Correction   
# =============================================================================


# =============================================================================
#	Open source file
# =============================================================================
if dst_filename is None:
    src_ds = gdal.Open( src_filename, gdal.GA_Update )
else:
    src_ds = gdal.Open( src_filename, gdal.GA_ReadOnly )
 
if src_ds is None:
    print('Unable to open %s' % src_filename)
    sys.exit(1)

# =============================================================================
#	get source file metadata 
# =============================================================================

if src_ds is None:
    print "Could not read file."
    Usage()
else:
    src_projection = src_ds.GetProjection()
    src_geotransform = src_ds.GetGeoTransform()
    src_datatype = src_ds.GetDriver().ShortName
   
    if not src_geotransform is None:
         print 'Origin = (',src_geotransform[0], ',',src_geotransform[3],')'
         print 'Pixel Size = (',src_geotransform[1], ',',src_geotransform[5],')'


def getBandNumber(source_filename):
   splitfilename_underscore = source_filename.split('_')
   # print splitfilename_underscore[len(splitfilename_underscore)-2]
  

   splitfilename_dot = splitfilename_underscore[len(splitfilename_underscore)-1].split('.')
   print splitfilename_dot[len(splitfilename_dot)-2]
   bandstring = splitfilename_dot[len(splitfilename_dot)-2]
   # bandstring = splitfilename_dot[len(splitfilename_dot)-2]
   # print bandstring[len(bandstring)-1]
   if bandstring == "B1":
    return 1
   elif bandstring == "B2":
    return 2 
   elif bandstring == "B3":
    return 3
   elif bandstring == "B4":
    return 4
   elif bandstring == "B5":
    return 5
   # elif bandstring == "B6_VCID_1":
   #  return 61
   # elif bandstring == "B6_VCID_2":
   #  return 62
   elif bandstring == "B7":
    return 7
   elif bandstring == "B8":
    return 8
   else:
    print "unable to read band number from filename string"
    return 0

bandInt = getBandNumber(src_filename)
print "bandid = " , bandInt 



# =============================================================================
#       Create output file if one is specified.
# =============================================================================

        