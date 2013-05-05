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
from math import *

#time
import re
import time

def Usage():
    print("""USAGE: openir_atmosphericcorrection.py [sourcefile] [dstfile] """)
    sys.exit(1)

from osgeo import osr, gdal





# =============================================================================
#      MTL file reader with Geotiff source filename as arguments 
# =============================================================================
def getMTLkeywordValueWithSourceFilename( mtl_keyword , source_filename ):
    mtl_filename_list  = source_filename.split(r"_", 1)
    mtl_filename = mtl_filename_list[0]
    mtl_filename+=("_MTL.txt")
    mtl_exists = os.path.exists( mtl_filename)
    if(mtl_exists):
       print ("MTL file found",  mtl_exists)
    else: 
       print ("MTL file not found")
       sys.exit(1)
	#read MTL file 
    mtl_content = ""
    with open(mtl_filename, 'r') as content_file:
	  mtl_content = content_file.read()

    for item in mtl_content.split("\n"):
       if mtl_keyword in item:
          return item.split(r" = ", 1)[1]

# =============================================================================
#      JULIAN DATE 
# =============================================================================
def getJulianDateWithDATE_ACQUIRED(date_acquired):
    (year, month, day) = DATE_ACQUIRED.split('-')
    year = int(year)
    month = int(month)
    day = int(day)
    t = time.mktime((year, month, day, 0, 0, 0, 0, 0, 0))
    time.gmtime(t)
    return time.gmtime(t)[7]

           
# Input values for LOW GAIN 
# GET LMIN WITH BANDID (GETBAND)
def getLminWithBand(bandID):
#Lmax values based on http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
	Lmin1 = -6.2
	Lmin2 = -6.4
	Lmin3 = -5.0
	Lmin4 = 5.1
	Lmin5 = -1.0
	Lmin6 = 0.0
	Lmin7 = -0.35
	Lmin8 = -4.7
	if bandID == 1:
		return Lmin1
	elif bandID == 2:
	      return Lmin2
	elif bandID == 3:
	      return Lmin3
	elif bandID == 4:
	      return Lmin4
	elif bandID == 5:
	      return Lmin5
	elif bandID == 61:
	      return Lmin61
	elif bandID == 62:
	      return Lmin62
	elif bandID == 7:
	      return Lmin7
	elif bandID == 8:
	      return Lmin8
	else:
	   print "getL-MIN-WithBand error"
	   return 0
            
# Input values for LOW GAIN 
# GET Lmax WITH BANDID (GETBAND) 
#Lmax values based on http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
#returns float from 1 to 8
def getLmaxWithBand(bandID):
	Lmax1 = 293.7
	Lmax2 = 300.9
	Lmax3 = 234.4
	Lmax4 = 241.1
	Lmax5 = 47.57
	Lmax6 = 17.04
	Lmax7 = 16.54
	Lmax8 = 243.1
	if bandID == 1:
		return Lmax1
	elif bandID == 2:
		return Lmax2
	elif bandID == 3:
		return Lmax3
	elif bandID == 4:
	    return Lmax4
	elif bandID == 5:
	    return Lmax5
	elif bandID == 61:
	    return Lmax6
	elif bandID == 62:
	    return Lmax6
	elif bandID == 7:
	    return Lmax7
	elif bandID == 8:
	    return Lmax8
	else: 
	    print "getL-MAX-WithBand error"
	    return 0

#Mean solar exoatmospheric irradiance in mW cm-2m m-1. ESUN can be obtained from Table 11.2 in http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html.      
def getSolarIrradianceWithBand(bandID):
    ESUN1 = 1997.0
    ESUN2 = 1812.0
    ESUN3 = 1530.0
    ESUN4 = 1039.0 
    ESUN5 = 230.8 
    ESUN6 = 000.0 
    ESUN7 = 84.90 
    ESUN8 = 1362.0
    if band == 1:
          return ESUN1
    elif band == 2:
          return ESUN2
    elif band == 3:
          return ESUN3
    elif band == 4:
          return ESUN4
    elif band == 5:
          return ESUN5
    elif band == 61:
          return ESUN6
    elif band == 62:
          return ESUN6
    elif band == 7:
          return ESUN7
    elif band == 8:
          return ESUN8
    else: 
          print "getL-MAX-WithBand error"
          return 0

#get bandID from file
def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    print band
    band = re.search('\\d',band).group(0)
    return int(band)

#degrees to radians 
def d2r(degree):
         return exp( degree* math.pi/180 )

def      SunEarthDistanceRatio(d_n):
       t=(2*pi* (d_n - 1) / 365);
       E_0=exp( (1.000110+ 0.034221* math.cos(t) + 0.001280* math.sin(t) + 0.000719* math.cos(2*t) + 0.000077* math.sin(2*t)) )
       return math.sqrt(exp(1/E_0))

# 
# # =============================================================================
# #       Create output file if one is specified.
# # =============================================================================
# def convertDNtoExoatmosphericReflectance(source_filename):
# 	   #function variables
# 	   bandID = getBand(source_filename)
# 	   Lmin = getLminWithBand(bandID)       
# 	   Lmax = getLmaxWithBand(bandID)
# 	   QCALMIN = 1 
# 	   QCALMAX = 255
# 	
# 	 # pending center lat lon
# 	  # CenterLon =  
# 	  #   CenterLat = 
# 		#!!!!!!############################################################################### pending DN parse function 
# 	  
# 	  
# 		#Step 1. Converting DN to at satellite spectral radiance (L) using formulae of the type:
# 		L = exp( Lmin+(Lmax/254-Lmin/255))
# 	
# 		
# 		# ARLENE NOTE: the code below is a different (more accurate)? way to calculate L, from http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
# 	  	# // NOTE: radiance is commonly notated as Llambda (where "lambda" is the band number)
# 		# // QCAL = digital number, based on image's greyscale value
# 		# // LMINlambda= spectral radiance scales to QCALMIN, 
# 		# // LMAXlambda = spectral radiance scales to QCALMAX
# 		# // QCALMIN = the minimum quantized calibrated pixel value (typically = 1, based on the images's MTL file)
# 		# // QCALMAX = the maximum quantized calibrated pixel value (typically = 255, based on the images's MTL file)
# 		# LMINL = exp( Lmin / QCALMIN )
# 		# LMAXL = exp( Lmax / QCALMAX )
# 		# L = exp(((lmax - LMINL)/(qcalmax-qcalmin))*(DN-qcalmin)+lmin)
# 	 
# 	 
# 	 
# 	  # Step 2. Converting at satellite spectral radiance (L) to exoatmospheric reflectance
# 	
# 	  #!!!!!!############################################################################### pending DATE_ACQUIRED parse function 
# 	  #REVISE the square of the Earth-Sun distance in astronomical units
# 	  # there is a distinct distance for every day of the year
# 	  #based on http://landsathandbook.gsfc.nasa.gov/excel_docs/d.xls
# 	  # var dcal = (1-0.01672*COS(RADIANS(0.9856*(Julian Day-4))))
# 	   dcal = exp( 1- 0.01672 * math.cos( math.radians( 0.9856 * (JulianDate -4 ))))
# 	  
# 	   #REVISE DATE BASED ON IMAGE
# 	   dsquared = math.sqrt(dcal)
# 	
# 	  #REVISE SUN ZENITH ANGLE BASED ON RADIANS
# 	  #23.5 is the tilt of the earth
# 	  #SZ = Latitude + (23.5 * cosine(JulianDate));
# 	  # SZ = 90-39 = 51- = 0.89012 radians
# 	  #SZ = 0.89012 ;
# 	   SZ = exp( LAT +  (23.5 * math.cos(JulianDate))) 
# 	  
# 	  # // reflectance or Rolamda = Unitless plantary reflectance
# 	  #     // radiance or Llamda= spectral radiance (from earlier step)
# 	  #     // d = Earth-Sun distance in astronmoical units 
# 	  #     // ESUNlamda = mean solar exoatmospheric irradiances 
# 	  #     // ths or thetas = solar zenith angle
# 	
# 	   ESUN = getSolarIrradianceWithBand()
# 	   R = exp( math.pi * L * dsquared / (ESUN * math.cos(SZ)) )
# 	  
# 	  # #Stage 2 of atmospheric correction using 5S radiative transfer model outputs
# 	  # AI = 1 / (Global gas transmittance * Total scattering transmittance)
# 	  # BI = - Reflectance / Total scattering transmittance
# 	  # 
# 	  # #Stage 3 of atmospheric correction using 5S radiative transfer model outputs
# 	  # (AI1 * @1 + BI1) / (1 + S1 * (AI1 * @1 + BI1) )
# 	  # 



# =============================================================================
#       Mainline
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
#      Setup Atmospheric Correction   
# =============================================================================


# =============================================================================
#      Open source file
# =============================================================================
if dst_filename is None:
    src_ds = gdal.Open( src_filename, gdal.GA_Update )
else:
    src_ds = gdal.Open( src_filename, gdal.GA_ReadOnly )
 
if src_ds is None:
    print('Unable to open %s' % src_filename)
    sys.exit(1)


if src_ds is None:
    print "Could not read file."
    Usage()
else:
    src_projection = src_ds.GetProjection()
    src_geotransform = src_ds.GetGeoTransform()
    src_datatype = src_ds.GetDriver().ShortName
    width = src_ds.RasterXSize
    height = src_ds.RasterYSize
    gt = src_ds.GetGeoTransform()
    minx = gt[0]
    miny = gt[3] + width*gt[4] + height*gt[5] 
    maxx = gt[0] + width*gt[1] + height*gt[2]
    maxy = gt[3]
    print 'minx  = (', minx, ')'
    print 'miny  = (', miny, ')'
    print 'maxx  = (', maxx, ')'
    print 'maxy  = (', maxy, ')'
	#get the coordinates in lat long
    old_cs= osr.SpatialReference()
    old_cs.ImportFromWkt(src_ds.GetProjectionRef())
	# create the new coordinate system
    wgs84_wkt = """
    GEOGCS["WGS 84",
        DATUM["WGS_1984",
            SPHEROID["WGS 84",6378137,298.257223563,
                AUTHORITY["EPSG","7030"]],
            AUTHORITY["EPSG","6326"]],
        PRIMEM["Greenwich",0,
            AUTHORITY["EPSG","8901"]],
        UNIT["degree",0.01745329251994328,
            AUTHORITY["EPSG","9122"]],
        AUTHORITY["EPSG","4326"]]"""
    new_cs = osr.SpatialReference()
    new_cs .ImportFromWkt(wgs84_wkt)
    # create a transform object to convert between coordinate systems
    transform = osr.CoordinateTransformation(old_cs,new_cs)


    LatLong = transform.TransformPoint(minx,miny)
    print 'LatLong = (', LatLong, ')'

    if not src_geotransform is None:
         print 'Origin = (',src_geotransform[0], ',',src_geotransform[3],')'
         print 'Pixel Size = (',src_geotransform[1], ',',src_geotransform[5],')'
 
DATE_ACQUIRED = getMTLkeywordValueWithSourceFilename( "DATE_ACQUIRED" ,  src_filename )
print "DATE_ACQUIRED of MTL FILE =" ,DATE_ACQUIRED


print "JULIAN DATE of MTL FILE = ", getJulianDateWithDATE_ACQUIRED(DATE_ACQUIRED) 
