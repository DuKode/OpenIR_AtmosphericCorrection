#!/usr/bin/env python2.7
#******************************************************************************
#  Name:     openir_atmosphericcorrection
#  Project:  OpenIR - GDAL Python Interface
#  Purpose:  atmospheric correction 
#  Author:   dukodestudio, info@dukodestudio.com
# GDAL PYTHON DOCUMENTATION http://gdal.org/python/
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

import numpy 

def Usage():
    print("""USAGpyhtonE: openir_atmosphericcorrection.py [sourcefile] [dstfile] """)
    sys.exit(1)

from osgeo import osr, gdal





# =============================================================================
#      MTL file reader with keyword and Geotiff source filename as arguments 
# =============================================================================
def getMTLkeywordValueWithSourceFilename( mtl_keyword , source_filename ):
    mtl_filename_list  = source_filename.split(r"_", 1)
    mtl_filename = mtl_filename_list[0]
    mtl_filename+=("_MTL.txt")
    mtl_exists = os.path.exists( mtl_filename)
    if(mtl_exists == 0):
       print ("MTL file not found")
       sys.exit(1)
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
    # units watts/(meter squared * nano-m)
    ESUN1 = 1997.0
    ESUN2 = 1812.0
    ESUN3 = 1530.0
    ESUN4 = 1039.0 
    ESUN5 = 230.8 
    ESUN6 = 000.0 
    ESUN7 = 84.90 
    ESUN8 = 1362.0

    if bandID == 1:
          return ESUN1
    elif bandID == 2:
          return ESUN2
    elif bandID == 3:
          return ESUN3
    elif bandID == 4:
          return ESUN4
    elif bandID == 5:
          return ESUN5
    elif bandID == 61:
          return ESUN6
    elif bandID == 62:
          return ESUN6
    elif bandID == 7:
          return ESUN7
    elif bandID == 8:
          return ESUN8
    else: 
          print "getL-MAX-WithBand error"
          return 0

#get bandID from file
def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    # print band
    band = re.search('\\d',band).group(0)
    return int(band)

#degrees to radians 
def d2r(degree):
         return exp( degree* math.pi/180 )

def      SunEarthDistanceRatio(d_n):
       t=(2*pi* (d_n - 1) / 365);
       E_0=exp( (1.000110+ 0.034221* math.cos(t) + 0.001280* math.sin(t) + 0.000719* math.cos(2*t) + 0.000077* math.sin(2*t)) )
       return math.sqrt(exp(1/E_0))


def CopyBand( srcband, dstband ):
    for line in range(srcband.YSize):
        line_data = srcband.ReadRaster( 0, line, srcband.XSize, 1 )
        dstband.WriteRaster( 0, line, srcband.XSize, 1, line_data,
                             buf_type = srcband.DataType )

# 
# # =============================================================================
# #       Create output file if one is specified.
# # =============================================================================
def convertDNtoExoatmosphericReflectance(DN, bandID):


   
   #function variables
   # bandID = getBand(source_filename)
   Lmin = getLminWithBand(bandID)       
   Lmax = getLmaxWithBand(bandID)
   QCALMIN = 1 
   QCALMAX = 255

 # pending center lat lon
  # CenterLon =  
  #   CenterLat = 
	#!!!!!!############################################################################### pending DN parse function 
  
  
	#Step 1. Converting DN to at satellite spectral radiance (L) using formulae of the type:
# 	2.1.1. Gain and Bias Method http://www.yale.edu/ceo/Documentation/Landsat_DN_to_Reflectance.pdf
#   L = gain * DN + bias 
# 2.1.2. Spectral Radiance Scaling Method http://www.yale.edu/ceo/Documentation/Landsat_DN_to_Reflectance.pdf
   # L = exp( Lmin+(Lmax/254-Lmin/255))	
   L = exp( ((Lmax - Lmin)/(QCALMAX - QCALMIN))*(DN-QCALMIN)+Lmin ) 

	# ARLENE NOTE: the code below is a different (more accurate)? way to calculate L, from http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
  	# // NOTE: radiance is commonly notated as Llambda (where "lambda" is the band number)
	# // QCAL = digital number, based on image's greyscale value
	# // LMINlambda= spectral radiance scales to QCALMIN, 
	# // LMAXlambda = spectral radiance scales to QCALMAX
	# // QCALMIN = the minimum quantized calibrated pixel value (typically = 1, based on the images's MTL file)
	# // QCALMAX = the maximum quantized calibrated pixel value (typically = 255, based on the images's MTL file)
	# LMINL = exp( Lmin / QCALMIN )
	# LMAXL = exp( Lmax / QCALMAX )
	# L = exp(((lmax - LMINL)/(qcalmax-qcalmin))*(DN-qcalmin)+lmin)
 
 
 
  # Step 2. Converting at satellite spectral radiance (L) to exoatmospheric reflectance

  #!!!!!!############################################################################### pending DATE_ACQUIRED parse function 
  #REVISE the square of the Earth-Sun distance in astronomical units
  # there is a distinct distance for every day of the year
  #based on http://landsathandbook.gsfc.nasa.gov/excel_docs/d.xls
  # var dcal = (1-0.01672*COS(RADIANS(0.9856*(Julian Day-4))))
   JulianDate = getJulianDateWithDATE_ACQUIRED(getMTLkeywordValueWithSourceFilename( "DATE_ACQUIRED" , src_filename ))
   if (JulianDate>=1 and JulianDate<15):
	d = 0.9832
   elif (JulianDate>=15 and JulianDate<32):
	d = 0.9836
   elif (JulianDate>=32 and JulianDate<46):
	d = 0.9853
   elif (JulianDate>=46 and JulianDate<60):
	d = 0.9878
   elif (JulianDate>=60 and JulianDate<74):
	d = 0.9878
   elif (JulianDate>=60 and JulianDate<74):
	d = 0.9909
   elif (JulianDate>=74 and JulianDate<91):
	d = 0.9945
   elif (JulianDate>=91 and JulianDate<106):
	d = 0.9993
   elif (JulianDate>=106 and JulianDate<121):
	d = 1.0033
   elif (JulianDate>=121 and JulianDate<135):
	d = 1.0076
   elif (JulianDate>=135 and JulianDate<152):
	d = 1.0109
   elif (JulianDate>=152 and JulianDate<166):
	d = 1.0140
   elif (JulianDate>=166 and JulianDate<182):
	d = 1.0158
   elif (JulianDate>=182 and JulianDate<196):
	d = 1.0167
   elif (JulianDate>=196 and JulianDate<213):
	d = 1.0165
   elif (JulianDate>=213 and JulianDate<227):
	d = 1.0149
   elif (JulianDate>=227 and JulianDate<242):
	d = 1.0128
   elif (JulianDate>=242 and JulianDate<258):
	d = 1.0092
   elif (JulianDate>=258 and JulianDate<274):
	d = 1.0057
   elif (JulianDate>=274 and JulianDate<288):
	d = 1.0011
   elif (JulianDate>=288 and JulianDate<305):
	d = 0.9972
   elif (JulianDate>=305 and JulianDate<319):
	d = 0.9925
   elif (JulianDate>=319 and JulianDate<335):
	d = 0.9892
   elif (JulianDate>=335 and JulianDate<349):
	d = 0.9860
   elif (JulianDate>=349 and JulianDate<365):
	d = 0.9843
   elif (JulianDate>=365):
	d = 0.9833
   else:
	print "Julian date greater than should ", JulianDate
	sys.exit(1)
   # d = exp()
   # dcal = exp( 1- 0.01672 * cos( radians( 0.9856 * ( JulianDate  -4 ))))
  
   #REVISE DATE BASED ON IMAGE
   # dsquared = sqrt(d)

  #REVISE SUN ZENITH ANGLE BASED ON RADIANS
  #23.5 is the tilt of the earth
  #SZ = Latitude + (23.5 * cosine(JulianDate));
  # SZ = 90-39 = 51- = 0.89012 radians
  #SZ = 0.89012 ;
   LAT = 39.35704080899672 
   LONG = -76.28388741488226
   SZ = exp( LAT +  (23.5 * cos(JulianDate))) 
  
  # // reflectance or Rolamda = Unitless plantary reflectance
  #     // radiance or Llamda= spectral radiance (from earlier step)
  #     // d = Earth-Sun distance in astronmoical units 
  #     // ESUNlamda = mean solar exoatmospheric irradiances 
  #     // ths or thetas = solar zenith angle

   ESUN = getSolarIrradianceWithBand(bandID)
   R = exp( pi * L * sqrt(d) / (ESUN * cos(SZ)) )
   # return R

   #Stage 2 of atmospheric correction using 5S radiative transfer model outputs
   #AI = 1 / (Global_gas_transmittance * Total_scattering_transmittance)
   #BI = - R / Total_scattering_transmittance
   AI = 1.2561 #TEST VALUES FOR BAND 1 FROM http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/images/Radcojun.frm
   BI = -0.0957 #TEST VALUES FOR BAND 1 FROM http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/images/Radcojun.frm

   intermediate_image_Y = exp(AI * R + BI) 
   #Stage 3 of atmospheric correction using 5S radiative transfer model outputs

   #S = Spherical albedo: TM1 = 0.167, TM2 = 0.121, TM3 = 0.092
   #Converting Y to surface reflectance (on scale 0-1) with formulae of the type:
   S1 = 0.167 #TEST VALUES FOR BAND 1 FROM http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/images/Radcojun.frm

   SR = exp(intermediate_image_Y / (1 + S1 * intermediate_image_Y))
   
   return SR 


class Printer():
    """Print things to stdout on one line dynamically"""
    def __init__(self,data):
        sys.stdout.write("\r\x1b[K"+data.__str__())
        sys.stdout.flush()
def format_seconds_to_hhmmss(seconds):
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02i:%02i:%02i" % (hours, minutes, seconds)


def getHistogramOffsetValue(source_ds):
  source_raster = source_ds.GetRasterBand(1)
  histogram = source_raster.GetHistogram( 1, 255,  256,  0,  1, None, None)
  histogram8bit =[]
  offsetValue = 0
  offsetIndex = 0
  addValue = 1 
  for i in range(len(histogram)):
     histogram8bit.append((histogram[i]%255)/10)
  
  print histogram8bit
  i=0
  while offsetValue<=addValue:
   i+=1
   offsetIndex = i 
   print "offsetIndex =", i 
   offsetValue+=histogram8bit[i]
   print "offsetValue =", offsetValue 
   addValue=histogram8bit[i]
   print "addValue =", addValue 
   offsetIndex=i 
 
  return  offsetIndex

def getDarkObjectFromImage(source_ds):
  source_raster = source_ds.GetRasterBand(1)
  dark_object = 255
  for i in range(source_raster.YSize):
    line_data = source_raster.ReadAsArray(0, i, source_raster.XSize, 1)
    for j in range(source_raster.XSize):
      current_pixel = line_data[0,j]
      if current_pixel < dark_object and current_pixel > 0:
        dark_object = current_pixel 
  return dark_object 

# =============================================================================
#       Mainline
# =============================================================================



quiet_flag = 0 #not used? 
src_filename = None #source file filename 
src_band = None #source file literal band - B1, B2, B3 etc. 

dst_filename = None #destination file filename 
format = 'GTiff' #format - we are only working with geotiff at the moment 
# creation_options = [] #not used.

gdal.AllRegister() #Register all known configured GDAL drivers. This function will drive any of the following that are configured into GDAL. Many others as well haven't been updated in this documentation (see full list):


########################### Start command line arguments parsing. 
argv = gdal.GeneralCmdLineProcessor( sys.argv )
if argv is None:
    sys.exit( 0 )

# ############################
# Parse command line arguments.
# ############################
i = 1
while i < len(argv):
    arg = argv[i]

    if arg == '-h':
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
########################## end command line arguments parsing. 



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
# #############################################################################
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
    # print 'minx  = (', minx, ')'
    # print 'miny  = (', miny, ')'
    # print 'maxx  = (', maxx, ')'
    # print 'maxy  = (', maxy, ')'
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
# #############################################################################


#create log file. 
import time
import datetime
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%dT%H-%M-%S')
logfile = open("log"+st+".txt", "w")


bands = src_ds.RasterCount
bandID = getBand(src_filename)
print "band id = " ,bandID 
DATE_ACQUIRED = getMTLkeywordValueWithSourceFilename( "DATE_ACQUIRED" ,  src_filename )
# print "DATE_ACQUIRED of MTL FILE =" ,DATE_ACQUIRED

#######################

srcband = src_ds.GetRasterBand(1)

drv = gdal.GetDriverByName(format)
dst_ds = drv.Create( dst_filename,src_ds.RasterXSize, src_ds.RasterYSize,1,
                    srcband.DataType)

# COPY GEOGRAPHIC INFO TO NEW FILE START
wkt = src_ds.GetProjection()
if wkt != '':
   dst_ds.SetProjection( wkt )

#set destination file geotransform to source geotransform 
dst_ds.SetGeoTransform( src_ds.GetGeoTransform() )
# COPY GEOGRAPHIC INFO TO NEW FILE  END 

#get destination raster image for band1 
dstband = dst_ds.GetRasterBand(1)


#### PIXEL MANIPULATION START 
pixelValueScaleFactor = 50
#read lines per columns 

rows = srcband.YSize
cols = srcband.XSize

nodata_value = 0 
nodate_value_result = srcband.SetNoDataValue(0)
print "nodate_value_result = ", nodata_value
print "nodata_value = ", nodata_value
# sys.exit(1)

processing_percentage = 0 
progress =  ("Processing file" + "." * int(processing_percentage))
sys.stdout.write('\r'+ progress)
start_time = time.time()

#dark object subtraction method
# DOS_pixel_value = getDarkObjectFromImage(src_ds)
# print "DOS_pixel_value = ", DOS_pixel_value 

#histogram methods 
offset_value = getHistogramOffsetValue (src_ds)
print "histogram offset value  = ", offset_value 
# sys.exit(1)

for i in range(srcband.YSize):
  line_data = srcband.ReadAsArray(0, i, srcband.XSize, 1)
  #read rows per line 
  #estimate progress percentage start  
  total_pixel = (srcband.YSize) 
  current_pixel = i+1
  processing_percentage = (current_pixel/(total_pixel*1.0)*100)
  # print ("hello", current_pixel/total_pixel)
  # print ("hello", exp(current_pixel/total_pixel))
  # print ("hello", float(current_pixel/total_pixel))
  # print "total_pixel " , total_pixel , "current_pixel ", current_pixel, "i ", i 


  for j in range(srcband.XSize):
	
    # pixel_value = convertDNtoExoatmosphericReflectance(line_data[0,j], getBand(src_filename))
    # pixel_value *=4 
    # if pixel_value < 0:
    #   print pixel_value
    
    #dos 
	# line_data[0 , j] = line_data[0 , j] - DOS_pixel_value
    #histogram 
    if (line_data[0,j]-offset_value) < 0:
      line_data[0,j] = 0
    else: 
      line_data[0, j] = line_data[0,j] - offset_value
	
  #write line_data to destination array 
  logfile.write("\n")
  dstband.WriteArray(line_data,0,i)
#### PIXEL MANIPULATION END 
  elapsedTime = -(start_time-(time.time()))
  output = "File processing  %f %% completed. Elapsed time %s hh:mm:ss, estimate completion at: %s" % (processing_percentage, format_seconds_to_hhmmss(-(start_time-(time.time()))), format_seconds_to_hhmmss( (100.0/processing_percentage)*-(start_time-time.time())) )  
# print (time.time() - start_time), "seconds"
  Printer(output)

# flush data to disk, set the NoData value and calculate stats
dstband.FlushCache()
dstband.SetNoDataValue(-99)
stats = dstband.GetStatistics(0, 1)

# georeference the image and set the projection
dst_ds.SetGeoTransform(src_ds.GetGeoTransform())
dst_ds.SetProjection(src_ds.GetProjection())

# build pyramids
gdal.SetConfigOption('HFA_USE_RRD', 'YES')
dst_ds.BuildOverviews(overviewlist=[2,4,8,16,32,64,128])

src_ds = None
dst_ds = None
#
