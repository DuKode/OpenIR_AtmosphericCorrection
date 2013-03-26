README.TXT
OpenIR Atmospheric Correction

With this project, we will try to translate this chapter on radiometric correction of satellite images:
http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/
Into a python script that processes one Landsat7 ETM+ Level 1 (L1) band image. The chapter uses TM imagery, so the values in its code must be replaced with ETM values: http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html

The python script will use commands from the Geospatial Data Abstraction Library (GDAL), which must be installed.
GDAL command reference: http://www.gdal.org/

TO GET STARTED, START EXPERIMENTING WITH PSEUDOCODE.TXT. WE'VE GONE THROUGH APPENDIX 3.1b and that should be ready to translate to Python.





MORE NOTES ON CONSTANTS USED
r= unitless planetary reflectance at the satellite (this takes values of 0-1.)

p= 3.141593

L = Spectral radiance at sensor aperture in mW cm-2 ster-1 m m-1

d2 = the square of the Earth-Sun distance in astronomical units = (1 - 0.01674 cos(0.9856 (JD-4)))2 where JD is the Julian Day (day number of the year) of the image acquisition. [Note: the units for the argument of the cosine function of 0.9856 x (JD-4) will be in degrees; if your cosine function (e.g. the cos function in Excel is expecting the argument in radians, multiply by p /180 before taking the cosine)].

ESUN = Mean solar exoatmospheric irradiance in mW cm-2m m-1. ESUN can be obtained from Table 3.5.

SZ = sun zenith angle in radians when the scene was recorded.








MORE OLD CODE FROM ILIAS


function getReflectanceValueWithDnumberGainAndBias(DN, gain, bias){
//DN to radiance....
//http://cwcaribbean.aoml.noaa.gov/bilko/module7/lesson3/
var gain = (lmax/254)-(lmin/255);
console.log("gain= " + gain);
var bias = lmin;
var radiance = (gain * DN) + bias;
// Lλ is the cell value as radiance
// DN is the cell value digital number
// gain is the gain value for a specific band
// bias is the bias value for a specific band

//radiance to reflectance....
//array[1] = band 1....array[2]= band2, array[0] = null
var ETMsolarspectralirradiances = [0, 1969.000, 1840.000, 1551.000, 1044.000, 225.700, 82.07, 1368.000];
var juliandate= [0,1,15,32,46,60,74,91,106,121, 135, 152, 166, 182, 196, 213, 227, 242, 258, 274, 288, 305, 319, 335, 349, 365];
var earthSunDistanceinAU = [0, .9832, .9836, .9853, .9878, .9909, 9945, .9993, 1.0033, 1.0076, 1.0109, 1.0140, 1.0158, 1.0167, 1.0165, 1.0149, 1.0128, 1.0092, 1.0057, 1.0011, .9972, .9925, .9892, .9860, .9843, .9833];

//var esun =
//var d =
//var ths =
var reflectance = Math.PI * radiance * pow(d, 2) /esun *Math.cos(ths)
// reflectance or ρλ = Unitless plantary reflectance
// radiance or Lλ= spectral radiance (from earlier step)
// d = Earth-Sun distance in astronmoical units
// ESUNλ = mean solar exoatmospheric irradiances
// ths or θs = solar zenith angle

}
function getReflectanceValueWithDnumberLminAndLmax(DN, Lmin, Lmax){
// !!!!!!
//http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html
//!!!!!!!
// GROUP = MIN_MAX_RADIANCE
// RADIANCE_MAXIMUM_BAND_1 = 191.600
lmax = 191.600;
// RADIANCE_MINIMUM_BAND_1 = -6.200
lmin = -6.200;
// RADIANCE_MAXIMUM_BAND_2 = 196.500
// RADIANCE_MINIMUM_BAND_2 = -6.400
// RADIANCE_MAXIMUM_BAND_3 = 152.900
// RADIANCE_MINIMUM_BAND_3 = -5.000
// RADIANCE_MAXIMUM_BAND_4 = 157.400
// RADIANCE_MINIMUM_BAND_4 = -5.100
// RADIANCE_MAXIMUM_BAND_5 = 31.060
// RADIANCE_MINIMUM_BAND_5 = -1.000
// RADIANCE_MAXIMUM_BAND_6_VCID_1 = 17.040
// RADIANCE_MINIMUM_BAND_6_VCID_1 = 0.000
// RADIANCE_MAXIMUM_BAND_6_VCID_2 = 12.650
// RADIANCE_MINIMUM_BAND_6_VCID_2 = 3.200
// RADIANCE_MAXIMUM_BAND_7 = 10.800
// RADIANCE_MINIMUM_BAND_7 = -0.350
// RADIANCE_MAXIMUM_BAND_8 = 243.100
// RADIANCE_MINIMUM_BAND_8 = -4.700
// END_GROUP = MIN_MAX_RADIANCE
// GROUP = MIN_MAX_PIXEL_VALUE
// QUANTIZE_CAL_MAX_BAND_1 = 255
qcalmax = 255;
// QUANTIZE_CAL_MIN_BAND_1 = 1
qcalmin = 1;
// QUANTIZE_CAL_MAX_BAND_2 = 255
// QUANTIZE_CAL_MIN_BAND_2 = 1
// QUANTIZE_CAL_MAX_BAND_3 = 255
// QUANTIZE_CAL_MIN_BAND_3 = 1
// QUANTIZE_CAL_MAX_BAND_4 = 255
// QUANTIZE_CAL_MIN_BAND_4 = 1
// QUANTIZE_CAL_MAX_BAND_5 = 255
// QUANTIZE_CAL_MIN_BAND_5 = 1
// QUANTIZE_CAL_MAX_BAND_6_VCID_1 = 255
// QUANTIZE_CAL_MIN_BAND_6_VCID_1 = 1
// QUANTIZE_CAL_MAX_BAND_6_VCID_2 = 255
// QUANTIZE_CAL_MIN_BAND_6_VCID_2 = 1
// QUANTIZE_CAL_MAX_BAND_7 = 255
// QUANTIZE_CAL_MIN_BAND_7 = 1
// QUANTIZE_CAL_MAX_BAND_8 = 255
// QUANTIZE_CAL_MIN_BAND_8 = 1
// END_GROUP = MIN_MAX_PIXEL_VALUE
var radiance = ((lmax - lmin)/(qcalmax-qcalmin))*(DN-qcalmin)+lmin;
// Lλ is the cell value as radiance
// QCAL = digital number
// LMINλ = spectral radiance scales to QCALMIN
// LMAXλ = spectral radiance scales to QCALMAX
// QCALMIN = the minimum quantized calibrated pixel value
// (typically = 1)
// QCALMAX = the maximum quantized calibrated pixel value
// (typically = 255)


//DATE_ACQUIRED = 1999-07-05
//SCENE_CENTER_TIME = 15:32:37.5846119Z
var d = 1.00928;
// calculate d programmatically ---> var dcal = (1-0.01672*COS(RADIANS(0.9856*(Julian Day-4))))
var esun = 1997;
// Table 11.3 ETM+ Solar Spectral Irradiances
// (generated using the Thuillier solar spectrum)
// Band watts/(meter squared * μm)
// 1 1997
// 2 1812
// 3 1533
// 4 1039
// 5 230.8
// 7 84.90
// 8 1362.
var ths = 99.0;
cosths = 0.2725
// var reflectance = (Math.PI * radiance * Math.pow(d, 2)) / (esun *Math.cos(ths));
var reflectance = (Math.PI * radiance * Math.pow(d, 2)) / (esun *cosths);

// reflectance or ρλ = Unitless plantary reflectance
// radiance or Lλ= spectral radiance (from earlier step)
// d = Earth-Sun distance in astronmoical units
// ESUNλ = mean solar exoatmospheric irradiances
// ths or θs = solar zenith angle
console.log("radiance: "+ radiance + " Brescalereflectance:" + reflectance );
return reflectance;
}
//functions
function getJD(mon,day,yr,hr,min,sec) {
var m=parseFloat(mon.value);
var d=parseFloat(day.value);
var y=parseFloat(yr.value);
var minute=parseFloat(min.value);
var hour=parseFloat(hr.value);
var second=parseFloat(sec.value);
if (m < 3) {
y=y-1;
m=m+12;
}
var A=Math.floor(y/100);
var B=2-A+Math.floor(A/4);
JD=Math.floor(365.25*(y+4716))+Math.floor(30.6001*(m+1))+d+B-1524.5;
JD=JD+hour/24.0+minute/1440.0+second/86400.0;
JD=Math.round(JD*1000000)/1000000;
return JD;
}
