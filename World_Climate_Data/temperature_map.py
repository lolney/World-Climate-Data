""" Creates a map of temperature predictions based on the standard atmospheric model and interpolation between stations"""

from django.conf import settings
settings.configure(MONGODB_NAME='stations', DATABASES={
   'default' : {
      'ENGINE' : 'django_mongodb_engine',
      'NAME' : 'stations'
   }
})

import urllib, itertools, os, json, gc
from threading import Thread
from scipy.interpolate import griddata
from core.models import Station
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime as time

# For each month / Each of min / max:
# Prepare average matrix:
def avgTempMatrix(res, rect, month, category):

	minlng, minlat, maxlng, maxlat = rect[0][0], rect[0][1], rect[1][0], rect[1][1];
	# Create a masiive matrix, with dimensions x*res X y*res,
	# where x and y are the dimensions of the query rect and res is the resolution in squares/mi

	# Query average temp for locations inside this rect
	qset = Station.objects.raw_query({'coordinates' : {'$within': { '$box' : rect}}});

	lnggrid, latgrid = np.mgrid[minlng:maxlng:res*5,
								 minlat:maxlat:res*5];


	points = np.zeros((len(qset), 2));
	elevs = np.zeros(len(qset));
	temps = np.zeros(len(qset));

	for i, record in enumerate(qset):
		r = getattr(record, category);

		temp = getattr(r, month);
		elev = record.elevation;
		coords = record.coordinates;

		points[i] = np.array(coords);
		elevs[i] = elev;
		temps[i] = temp;

	#points = map(lambda x : x.coordinates, qset);
	#temps = map(lambda x : getattr(getattr(x, category), month), qset);
	#elevs = map(lambda x : x.elevation, qset);

	# Nearest neighbor interpolate to fill out matrix (both elevation and temperature)
	temperature = griddata(points, temps, (lnggrid, latgrid), method='linear');
	elevation 	= griddata(points, elevs, (lnggrid, latgrid), method='linear');
	# TODO: fill in holes

	return elevation, temperature;


def doQueries(lnggrid, latgrid, pointsList, valuesList, index):
	points = np.zeros((lnggrid.flatten().shape[0], 2));
	values = np.zeros_like(lnggrid.flatten());

	i = 0;
	it = iter(zip(lnggrid.flatten(), latgrid.flatten()));
	while True:
		try:
			lng, lat = it.next();

			query = {
				'x' : lng,
				'y' : lat,
				'units' : 'Feet',
				'output' : 'json'
			};

			points[i,:] = np.array([lng, lat]);

			qs = urllib.urlencode(query);
			response_str = urllib.urlopen("http://ned.usgs.gov/epqs/pqs.php?" + qs).read(); 
			response = json.loads(response_str);
			elevation = float(response['USGS_Elevation_Point_Query_Service']['Elevation_Query']['Elevation']);
			if elevation != -1000000: # error code
				values[i] = elevation;
			else:
				values[i] = 0;
			i+=1;

		except (StopIteration, KeyboardInterrupt):
			break;
		except:
			print 'Error; trying again';
			continue;
		

		if(i % 100 == 0):
			print i

	pointsList[index] = points;
	valuesList[index] = values;

def elevationMatrix(res, rect):	

	minlng, minlat, maxlng, maxlat = rect[0][0], rect[0][1], rect[1][0], rect[1][1];

	nt = 16;
	pointsList = [None] * nt;
	valuesList = [None] * nt;
	threads = [None] * nt;

	# This takes an astronomically long time (at about .5 seconds per request), but there doesn't
	# seem to be a better API for doing this
	start = time.now();
	for i in range(nt):	
		# Query elevation for locations inside this rect
		dlng = maxlng - minlng;
		dlat = maxlat - minlat;
		lnggrid, latgrid = np.mgrid[minlng + i*dlng/nt: minlng + (i+1)*dlng/nt:res/nt,
									minlat:maxlat:res];
		threads[i] = Thread(target=doQueries, args=(lnggrid, latgrid, pointsList, valuesList, i));
		threads[i].start();

	lnggrid, latgrid = np.mgrid[minlng:maxlng:res*5,
								minlat:maxlat:res*5];

	points, values = np.zeros((0,2)), np.zeros(0);
	for i, thread in enumerate(threads):
		thread.join();
		points = np.concatenate((points, pointsList[i]));
		values = np.concatenate((values, valuesList[i]));
	print points
	print values

	# Nearest neighbor interpolate to fill out matrix
	grid = griddata(points, values, (lnggrid, latgrid), method='linear');
	print time.now()-start;

	plt.imshow(grid.T, extent=(minlng,maxlng,minlat,maxlat), origin='lower');
	plt.show();

	return grid;

# Prepare elevation matrix:
def modeledTemperature(interpolated_elev, interpolated_temp, actual_elev):

	# For each point in the elev matrix, calculate expected temperature for that point 
		# deltaE = actual elevation - expected
	deltaE = actual_elev - interpolated_elev;
		# Standard atmospheric model: temp = expectedTemp + -0.0019812 * deltaE (in feet)
		#									 				-0.0065 * deltaE (in meters)
	temp = interpolated_temp - (0.0065 * deltaE);

	return temp;



months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
c = ['mins','maxes']
res = 2000j;
rect = [[-125.5, 24.0], [-95.5, 50.0]];#[[-125.5, 24.0], [-66, 50.0]]; # bounding rect for US

directory = 'maps';
if not os.path.exists(directory):
    os.makedirs(directory)

with open('maps/elevationMap1.npz') as w:#, open('maps/elevationMapEast.npz') as e:
	west = np.load(w);
	#actual_elev = np.concatenate((np.load(w), np.load(e)));

"""
actual_elev = elevationMatrix(res, rect);
with open('maps/elevationMapEast.npz', 'w+') as fd:
	np.save(fd, actual_elev);

"""
for month, cat in itertools.product(months, c):
	gc.collect();
	interpolated_elev, interpolated_temp = avgTempMatrix(res, rect, month, cat);
	gc.collect();
	result = modeledTemperature(interpolated_elev, interpolated_temp, actual_elev);
	with open('maps/' + str(month) + '_' + str(cat) + '.npz', 'w+') as fd:
		np.save(fd, result);

	#plt.imshow(np.flipud(result.T), origin='lower');
	#plt.show();





