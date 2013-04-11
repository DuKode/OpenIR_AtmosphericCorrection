import re
import gdal
from gdalconst import *

def getDate(filename):
	result = []
	regex = re.compile(r"""
		 \s*                 # Skip leading whitespace
		 DATE_ACQUIRED\s+=\s+
		 (?P<date>[^:]+)   # Header name
		 \s*$                # Trailing whitespace to end-of-line
		""", re.VERBOSE)
	with open(filename) as f:
		for line in f:
			match = regex.match(line)
			if match:
				result.append([
					match.group("date"),
					# etc.
				])
			
