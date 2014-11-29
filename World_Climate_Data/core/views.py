import json, random, math
from django.http import HttpResponse
from models import Station

def calcColor(temp):
	heatscale = int(((temp + 50.0) / 100.0) * 256)
	hex_color = '#%02x%02x%02x' % (heatscale, 128, 256 - heatscale)
	return hex_color

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
	# Process responce
	print qset;
	responses = [];
	for record in qset:
		coords = record.coordinates 
		name = record.StationName
		min_ = record.mins.Jan
		max_ = record.maxes.Jan

		
		temp = float(min_) if query['min'] == 'true' else float(max_);

		hex_color = calcColor(temp);
		if query['celsius'] != 'true':
				temp = temp * 9 / 5 + 32
		symbol = str(int(max(temp,0)))

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
							"marker-symbol": symbol
						}
					}
		responses.append(data);
	return HttpResponse(json.dumps(responses), content_type = "application/json")
