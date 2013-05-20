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
    
    driver.Create("cpy" + filename,inDS.RasterXSize,inDS.RasterYSize,1, band.DataType)
    outDS = gdal.Open("cpy" + filename)
    outDS.SetProjection(inDS.GetProjection())
    outDS.SetGeoTransform(inDS.GetGeoTransform())

   
    outBand = outDS.GetRasterBand(1)
    outdata = numpy.zeros((64,64))
    data = None

    i = 0
    blockysize = 64
    blockxsize = 64
    print inDS.RasterYSize
    while i <= xrange(inDS.RasterYSize):
        j = 0
        while j <= xrange(inDS.RasterXSize):
            yend = i + 64
            xend = j + 64
            if (i + 64) >= inDS.RasterYSize or (j +64 ) >= inDS.RasterXSize: 
                break
            data = numpy.array(band.ReadAsArray(j,i,64,64))
            if data == None:
                break
            for row in xrange(len(data)):
                if data[0] == None:
                    break
                for col in xrange(len(data[0])):
                    if data[row][col] + amount > 255:
                         #data[row][col] = 255
                         outdata[row][col] = 255
                    else:
                        #data[row][col] = data[row][col] + amount
                        outdata[row][col] = data[row][col] + amount
            outBand.WriteArray(outdata,j,i)
            j = j + 64
        i = i + 64

    outBand.FlushCache()
    outBand.SetNoDataValue(-99)

    gdal.SetConfigOption('HFA_USE_RRD', 'YES')
    outDS.BuildOverviews(overviewlist=[2,4,8,16,32,64,128])
    
    print "written"

    j = 0    
    while j <= xrange(inDS.RasterYSize):
        rowsize = 10
        if rowsize+j > inDS.RasterYSize:
            rowsize = inDS.RasterYSize - j - 1
            if rowsize == 0:
                break
        print outBand.ReadAsArray(0,j,inDS.RasterXSize/2,1)
      
        j = j + 10
 


    
    
##Returns the values of the band as an int. If something has failed it returns a null value.

def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    band = re.search('\\d',band).group(0)
    if band == None:
        sys.exit(1)
    return int(band)


changePixelData("LE70140321999186EDC00_B1.TIF",200)
    
