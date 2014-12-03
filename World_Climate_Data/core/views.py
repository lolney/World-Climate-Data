import json, random, math
from django.http import HttpResponse
from models import Station
import matplotlib as plt
import matplotlib.cm as cm

def calcColor(temp):
	norm = plt.colors.Normalize(vmin=-50, vmax=50)

	m = cm.ScalarMappable(norm=norm, cmap=cm.jet)
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
		qset = Station.objects.raw_query({'coordinates' : {'$within': { '$box' : [SW, NE]}}}).order_by('StationName')[:100]
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
