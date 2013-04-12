import re
import gdal
import struct
import sys
from gdalconst import *

def getData(filename):
    dataset = gdal.Open( filename, GA_ReadOnly )
    if dataset is None:
        print "Could not read file."
        return None
    else:
        print 'Driver: ', dataset.GetDriver().ShortName,'/', \
          dataset.GetDriver().LongName
        print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, \
          'x',dataset.RasterCount
        print 'Projection is ',dataset.GetProjection()
    
        geotransform = dataset.GetGeoTransform()
    if geotransform is None:
        print "There is something wrong with the metadata"
        return None
    else:
        print 'Origin = (',geotransform[0], ',',geotransform[3],')'
        print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'

def getPixelData(filename):
    dataset = gdal.Open(filename)
    if dataset is None:
        print "Could not read file."
        return None
    bandnumber = getBand(filename)
    if bandnumber == None:
        print "Could not get band"
        return None
    band = dataset.GetRasterBand(bandnumber)
    pixelarray = band.ReadAsArray(0,0,100,150)
    for row in pixelarray:
        for pixel in row:
            sys.stdout.write(pixel)
        print(" ")
    dataset = None
    ##scanline = band.ReadRaster(0,0, band.GetMinimum(),1,band.GetXSize(),1,GDT_FLOAT32)
    ##data = struct.unpack('f' * band.Xsize,scanline)
    ##print data
    
    
    
    
##Returns the values of the band as an int. If something has failed it returns a null value.

def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    band = re.search('\\d',band).group(0)
    if band == None:
        return None
    return int(band)