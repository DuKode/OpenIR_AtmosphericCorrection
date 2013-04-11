import re
import gdal
from gdalconst import *

def getData(filename):
    dataset = gdal.Open( filename, GA_ReadOnly )
    if dataset is None:
        return "Could not read file."
    else:
        print 'Driver: ', dataset.GetDriver().ShortName,'/', \
          dataset.GetDriver().LongName
        print 'Size is ',dataset.RasterXSize,'x',dataset.RasterYSize, \
          'x',dataset.RasterCount
        print 'Projection is ',dataset.GetProjection()
    
        geotransform = dataset.GetGeoTransform()
        if not geotransform is None:
            print 'Origin = (',geotransform[0], ',',geotransform[3],')'
            print 'Pixel Size = (',geotransform[1], ',',geotransform[5],')'
    ##Getting the bands
    
def getBand(filename):
    band = re.search('B\\d',filename).group(0)
    print band
    band = re.search('\\d',band).group(0)
    return int(band)
    
    
