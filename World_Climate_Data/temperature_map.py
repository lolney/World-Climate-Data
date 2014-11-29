from django.conf import settings
if not settings.configured:
    settings.configure()

import urllib, itertools, os, json
from scipy.interpolate import griddata
from core.models import Station
import numpy as np
import matplotlib.pyplot as plt

# For each month / Each of min / max:
# Prepare average matrix:
def avgTempMatrix(res, rect, month, category):

	minlng, minlat, maxlng, maxlat = rect[0][0], rect[0][1], rect[1][0], rect[1][1];
	# Create a masiive matrix, with dimensions x*res X y*res,
	# where x and y are the dimensions of the query rect and res is the resolution in squares/mi

	# Query average temp for locations inside this rect
	qset = Station.objects.raw_query({'coordinates' : {'$within': { '$box' : rect}}});

	lnggrid, latgrid = np.mgrid[minlng:maxlng:res,
								 minlat:maxlat:res];

	points = np.zeros((lnggrid.flatten().shape[0], 2));
	values = np.zeros_like(lnggrid.flatten());

	for i, record in enumerate(qset):
		r = getattr(record, category);

		temp = getattr(r, month);
		elev = record.elevation;
		coords = record.coordinates;

		points[i] = np.array(coords);
		elevs[i] = elev;
		temps[i] = temp;

	# Nearest neighbor interpolate to fill out matrix (both elevation and temperature)
	elevation 	= griddata(points, elev, (lnggrid, latgrid), method='nearest');
	temperature = griddata(points, temp, (lnggrid, latgrid), method='nearest');

	return elevation, temperature;

	
def elevationMatrix(res, rect):	

	minlng, minlat, maxlng, maxlat = rect[0][0], rect[0][1], rect[1][0], rect[1][1];

	# Query elevation for locations inside this rect
	lnggrid, latgrid = np.mgrid[minlng:maxlng:res,
								 minlat:maxlat:res];

	points = np.zeros((lnggrid.flatten().shape[0], 2));
	values = np.zeros_like(lnggrid.flatten());

	i = 0;
	for lng, lat in zip(lnggrid.flatten(), latgrid.flatten()):

		query = {
			'x' : lng,
			'y' : lat,
			'units' : 'Feet',
			'output' : 'json'
		};

		qs = urllib.urlencode(query);
		response_str = urllib.urlopen("http://ned.usgs.gov/epqs/pqs.php?" + qs).read();
		response = json.loads(response_str);

		elevation = float(response['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']);

		points[i,:] = np.array([lng, lat]);
		if elevation != -1000000: # error code
			values[i] = elevation;
		else:
			values[i] = 0;
		i+=1;

		if(i % 100 == 0):
			print i

	# Nearest neighbor interpolate to fill out matrix
	grid = griddata(points, values, (lnggrid, latgrid), method='linear');

	print grid;

	plt.imshow(grid.T, extent=(0,1,0,1), origin='lower');
	plt.show();

	return grid;

# Prepare elevation matrix:
def modeledTemperature(interpolated_elev, interpolated_temp, actual_elev):

	# For each point in the elev matrix, calculate expected temperature for that point 
		# deltaE = actual elevation - expected
	deltaE = actual_elev - interpolated_elev;
		# Standard atmospheric model: temp = expectedTemp + -0.0019812 * deltaE (in feet)
		#									 				-0.0065 * deltaE (in meters)
	temp = interpolated_temp - (0.0019812 * deltaE);
	return temp;


months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
c = ['mins','maxes']
res = 1000j;
rect = [[-126.604574, 24.885026], [-65.256916, 50.0]]; # bounding rect for US

directory = 'maps';
if not os.path.exists(directory):
    os.makedirs(directory)

actual_elev = elevationMatrix(res, rect);
with open('maps/elevationMap.npz', 'w+') as fd:
	np.save(fd, actual_elev);
"""
for month, cat in itertools.product(months, c):
	interpolated_elev, interpolated_temp = avgTempMatrix(res, rect, month, category);
	result = modeledTemperature(interpolated_elev, interpolated_temp, actual_elev);
"""



