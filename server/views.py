import json, random, math
from django.http import HttpResponse
from models import Station
import matplotlib as plt
import matplotlib.cm as cm
import numpy as np

def calcColor(temp):
	norm = plt.colors.Normalize(vmin=-40, vmax=40)

	C = np.array([[121,0,104],
				[119,0,112],
				[117,0,119],
				[115,0,126],
				[112,0,133],
				[110,0,141],
				[108,0,148],
				[106,0,155],
				[104,0,162],
				[102,0,170],
				[100,0,177],
				[98,0,184],
				[96,0,191],
				[94,0,199],
				[92,0,206],
				[90,0,213],
				[87,3,219],
				[82,16,222],
				[76,30,224],
				[71,43,226],
				[65,56,228],
				[59,69,231],
				[54,82,233],
				[48,96,235],
				[42,109,238],
				[37,122,240],
				[31,135,242],
				[25,148,245],
				[20,162,247],
				[14,175,249],
				[8,188,252],
				[3,201,254],
				[7,207,247],
				[22,205,231],
				[36,202,215],
				[51,200,198],
				[65,198,182],
				[80,196,166],
				[94,194,150],
				[109,192,134],
				[123,190,117],
				[137,187,101],
				[152,185,85],
				[166,183,69],
				[181,181,53],
				[195,179,36],
				[210,177,20],
				[224,174,4],
				[227,166,0],
				[226,155,0],
				[224,144,0],
				[223,132,0],
				[221,121,0],
				[220,110,0],
				[219,99,0],
				[217,88,0],
				[216,77,0],
				[215,66,0],
				[213,55,0],
				[212,44,0],
				[210,33,0],
				[209,22,0],
				[208,11,0],
				[206,0,0]])

	my_cmap = plt.colors.ListedColormap(C/256.0);
	m = cm.ScalarMappable(norm=norm, cmap=my_cmap)
	rgb = m.to_rgba(temp)[0:3];
	rgb = map(lambda x : int(x * 255), rgb);
	return '#%02x%02x%02x' % tuple(rgb);

def toFahrenheit(temp):
	return round(temp * 9 / 5 + 32, 1);

def main_display(request):
	
	query = request.GET;
	# Do geospatial query
	month = query['month']
	here = [float(x.encode('ascii', 'ignore')) for x in query['coordinates'].split(',')]
	NE = [float(x) for x in query['NE'].split(',')]
	SW = [float(x) for x in query['SW'].split(',')]

	try:
		print NE, SW
		qset = Station.objects.raw_query({'coordinates' : {'$within': { '$box' : [SW, NE]}}}).order_by('StationName')[:80]
		print len(qset)
	except:
		print 'Query error'
	# Process response
	responses = [];
	for record in qset:
		coords = record.coordinates 
		name = record.StationName
		min_ = getattr(record.mins, month)
		max_ = getattr(record.maxes, month)

		
		temp = float(min_) if query['min'] == 'true' else float(max_);

		# This slows down response substancially
		hex_color = calcColor(temp);
		if query['celsius'] != 'true':
				temp = toFahrenheit(temp)

		data = {
					'type': 'Feature', 
					'geometry':
						{
							'type': 'Point',
							'coordinates': coords
						},
					'properties': 
						{ 
							'title': name,
							'description': str(temp),
							'marker-size': 'large',
							'marker-color': hex_color,
							"marker-symbol": str(int(max(temp,0)))
						}
					}
		responses.append(data);
	return HttpResponse(json.dumps(responses), content_type = "application/json")
