import urllib2
from matplotlib.mlab import griddata

# For each month / Each of min / max:
# Prepare average matrix:
def avgTempMatrix(res, minlng, maxlng, minlat, maxlat):
	# Define quey rect (for locations in the US)

	# Create a masiive matrix, with dimensions x*res X y*res,
	# where x and y are the dimensions of the query rect and res is the resolution in squares/mi

		# Query average temp for locations inside this rect

		# Nearest neighbor interpolate to fill out matrix

	
def elevationMatrix(res, minlng, maxlng, minlat, maxlat):	
	# Query elevation for locations inside this rect
	lnggrid, latgrid = np.mgrid[minlng:maxlng:res,
								 minlat:maxlat:res];

	points = np.zeros(lnggrid.flatten().shape, 2);
	values = np.zeros(lnggrid.flatten().shape);

	for lng, lat in zip(lnggrid.flatten(), latgrid.flatten()):

		query = {
			'x' : lng,
			'y' : lat,
			'units' : 'feet',
			'output' : 'JSON'
		};

		qs = urllib.urlencode(query);
		response = urllib2.urlopen("ned.usgs.gov/epqs/pqs.php" + qs).read();

		points[i,:] = np.array([lng, lat]);
		values[i] = response['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation'];

	# Nearest neighbor interpolate to fill out matrix
	grid = griddata(points, values, (lnggrid, latgrid), method='linear');

	return grid.filled();

# Prepare elevation matrix:
def modeledTemperature(interpolated_temp, interpolated_elev, actual_elev):

	# For each point in the elev matrix, calculate expected temperature for that point 
		# deltaE = actual elevation - expected
	deltaE = actual_elev - interpolated_elev;
		# Standard atmospheric model: temp = expectedTemp + -0.0019812 * deltaE (in feet)
		#									 				-0.0065 * deltaE (in meters)
	temp = interpolated_temp - (0.0019812 * deltaE);

