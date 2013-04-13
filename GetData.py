import re
import gdal
import struct
import sys
import numpy
from gdalconst import *

def getData(filename):
    dataset = gdal.Open( filename, GA_ReadOnly )
    if dataset is None:
        print "Could not read file."
        sys.exit(1)
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

#fetchs the pixel data of the file. Does it in a for loop and one line at a time
#filename is the name of the file. must have a B followed by a number stating the band

def changePixelData(filename,amount):
    
    inDS = gdal.Open(filename)
    bandnumber = getBand(filename)       
    band = inDS.GetRasterBand(bandnumber)
    driver = inDS.GetDriver()
    
    driver.Create("cpy" + filename, inDS.RasterXSize, inDS.RasterYSize,bandnumber, GDT_UInt16)
    outDS = gdal.Open("cpy" + filename)
    outBand = outDS.GetRasterBand(bandnumber)
    outdata = [[]]
    data = [[]]

    i = 0
    while i <= xrange(inDS.RasterYSize):
        rowsize = 10
        if rowsize+i > inDS.RasterYSize:
            rowsize = inDS.RasterYSize - i - 1
            if rowsize == 0:
                break
        data = band.ReadAsArray(0,i,inDS.RasterXSize,10)
        outBand.WriteArray(data,0,i)
        i = i + 10
	

    outdata = outBand.ReadAsArray(0,0,inDS.RasterXSize, 3)
    for row in xrange(len(outdata)):
        for col in xrange(len(outdata)):
            if not data[row][col] == outdata[row][col]:
                print row
                print col
                print data[row][col]
                print outdata[row][col]
                return False
        
    outDS.SetProjection(inDS.GetProjection())
    outDS.SetGeoTransform(inDS.GetGeoTransform())
            
    return True


    
    
##Returns the values of the band as an int. If something has failed it returns a null value.

def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    band = re.search('\\d',band).group(0)
    if band == None:
        sys.exit(1)
    return int(band)



    
