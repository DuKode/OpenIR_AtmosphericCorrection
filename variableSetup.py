#Appendix 3.1a: Steps 1-2 of radiometric correction. Converting DN values to exoatmospheric reflectance
# Ilias Note: additional resources for color correction http://code.google.com/p/xatmcorr/source/browse/trunk/src/main.cpp?r=31
# http://code.google.com/p/xatmcorr/source/browse/trunk/src/dntotoa.cpp?r=31


# Step 1. Converting DN to at satellite spectral radiance (L) using formulae of the type:

Lmin + (Lmax/254 - Lmin/255) * @n ;


# Input values for LOW GAIN 
# (Arlene Note: see http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html, Table 11.2)
# Lmin: ETM1 = -6.2, ETM2 = -6.4, ETM3 = -5.0, ETM4 = 5.1, ETM5 = -1.0, ETM6 = 0.0, ETM7 = -0.35, ETM8 = -4.7
# Lmax: ETM1 = 293.7, ETM2 = 300.9, ETM3 - 234.4, ETM4 = 241.1, ETM5 = 47.57, ETM6 = 17.04, ETM7 = 16.54, ETM8 = 243.1


#BLOCK BELOW IS REVISED FROM ETM VALUES ABOVE.
const_Lmin1 = -6.2;
const_Lmin2 = -6.4;
const_Lmin3 = -5.0;
const_Lmin4 = -5.1;
const_Lmin5 = -1.0;
const_Lmin6 = -0.0;
const_Lmin7 = -0.35;
const_Lmin8 = -4.7;

const_Lmax1 = 293.7;
const_Lmax2 = 300.9;
const_Lmax3 = -234.4;
const_Lmax4 = 241.1;
const_Lmax5 = 47.57;
const_Lmax6 = 17.04;
const_Lmax7 = 16.54;
const_Lmax8 = 243.1;




# NOTE: radiance is commonly notated as Lλ (where "λ" is the band number)
# QCAL = digital number, based on image's greyscale value
# LMINλ  = spectral radiance scales to QCALMIN, 
# LMAXλ = spectral radiance scales to QCALMAX
# QCALMIN = the minimum quantized calibrated pixel value (typically = 1, based on the images's MTL file)
# QCALMAX = the maximum quantized calibrated pixel value (typically = 255, based on the images's MTL file))	
var radiance = ((lmax - lmin)/(qcalmax-qcalmin))*(DN-qcalmin)+lmin;




# Step 2. Converting at satellite spectral radiance (L) to exoatmospheric reflectance


# Input values
# ==========

 pi = 3.141593

#REVISE the square of the Earth-Sun distance in astronomical units
# there is a distinct distance for every day of the year
#based on http://landsathandbook.gsfc.nasa.gov/excel_docs/d.xls
d? = ---
#REVISE DATE BASED ON IMAGE
const dsquared = -- ;

#REVISE SUN ZENITH ANGLE BASED ON RADIANS
#23.5 is the tilt of the earth
#SZ = Latitude + (23.5 * cosine(JulianDate));
# SZ = 90-39 = 51- = 0.89012 radians
const SZ = 0.89012 ;

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

#Mean solar exoatmospheric irradiance in mW cm-2m m-1. ESUN can be obtained from Table 11.2 in http://landsathandbook.gsfc.nasa.gov/data_prod/prog_sect11_3.html.
const_ESUN1 = 1997;
const_ESUN2 = 1812 ;
const_ESUN3 = 1530 ;
const_ESUN4 = 1039 ;
const_ESUN5 = 230.8 ;
const_ESUN6 = --- ;
const_ESUN7 = 84.90 ;
const_ESUN8 = 1362 ;




# Let at satellite spectral radiance = L (see intermediate formulae above)

# Converting L to exoatmospheric reflectance (on scale 0-1) with formulae of the type:


# pi * L * dsquared / (ESUN * cos(SZ)) ;

#

pi * (Lmin1 + (Lmax1/254 - Lmin1/255)*@1) * dsquared / (ESUN1 * cos(SZ)) ;

pi * (Lmin2 + (Lmax2/254 - Lmin2/255)*@2) * dsquared / (ESUN2 * cos(SZ)) ;

pi * (Lmin3 + (Lmax3/254 - Lmin3/255)*@3) * dsquared / (ESUN3 * cos(SZ)) ; 
  
  
  
  
  
  
  
  
  
  
  

Appendix 3.1b: Step 3 of radiometric correction (Stages 2-3 of atmospheric correction).

# 1-3 collected over the Turks and Caicos on 22 November 1990.

#

# Formula document 2.

# =================

# Stage 2 of atmospheric correction using 5S radiative transfer model outputs

#

# Input values

# ==========

# AI = 1 / (Global gas transmittance * Total scattering transmittance)

# TM1 = 1.3056, TM2 = 1.2769, TM3 = 1.1987

#

# BI = - Reflectance / Total scattering transmittance

# TM1 = -0.0992, TM2 = -0.0515, TM3 = -0.0301

#

const AI1 = 1.3056 ;

const AI2 = 1.2769 ;

const AI3 = 1.1987 ;

const BI1 = -0.0992 ;

const BI2 = -0.0515 ;

const BI3 = -0.0301 ;

# Let exoatmospheric reflectance = @n (i.e. images output by first formula document)

#

# Converting exoatmospheric reflectance (scale 0-1) to intermediate image Y with formulae of the type:

# AI * @n + BI;

#

# Intermediate formulae for Y:

#

# AI1 * @1 + BI1;

# AI2 * @2 + BI2;

# AI3 * @3 + BI3;

#

# Stage 3 of atmospheric correction using 5S radiative transfer model outputs

#

# Input values

# ==========

# S = Spherical albedo: TM1 = 0.156, TM2 = 0.108, TM3 = 0.079

#

const S1 = 0.156 ;

const S2 = 0.108 ;

const S3 = 0.079 ;

# Let intermediate image = Y (see intermediate formulae above)

#

# Converting Y to surface reflectance (on scale 0-1) with formulae of the type:

#

# Y / (1 + S * Y) ;

#

(AI1 * @1 + BI1) / (1 + S1 * (AI1 * @1 + BI1) ) ;

(AI2 * @2 + BI2) / (1 + S2 * (AI2 * @2 + BI2) ) ;

(AI3 * @3 + BI3) / (1 + S3 * (AI3 * @3 + BI3) ) ; 
