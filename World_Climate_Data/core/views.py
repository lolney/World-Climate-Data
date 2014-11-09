import json, random
from django.http import HttpResponse

def ajax(request):
	with open('/Users/Luke/World-Climate-Data/World_Climate_Data/core/data_with_coords.txt', 'rb') as jsonfile:
		#TODO: user requests month
		month = 0;

		jsonobj = json.load(jsonfile);
		records = jsonobj['records']
		responses = []
		# If len < threshold, cull
		thresh = 100
		random.shuffle(records);
		for record in records[0:thresh]:

			coords = record['coordinates'] if record['coordinates'] is not None else [0,0]
			name = record['Station Name'] if record['Station Name'] is not None else 'No name'
			min_ = record['mins']['Jan']
			max_ = record['maxes']['Jan']

			temp = int(((float(min_) + 50.0) / 100.0) * 256)
			hex_color = '#%02x%02x%02x' % (temp, 128, 256 - temp)

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
							'description': str(min_),
							'marker-size': 'large',
							'marker-color': hex_color
						}
					}
			responses.append(data);
		return HttpResponse(json.dumps(responses), content_type = "application/json")