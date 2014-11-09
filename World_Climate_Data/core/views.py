import json, random, math
from django.http import HttpResponse

def ajax(request):
	with open('/Users/Luke/World-Climate-Data/World_Climate_Data/core/data_with_coords.txt', 'rb') as jsonfile:
		query = request.GET;
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

			temp = float(min_) if query['min'] != 'true' else float(max_);

			heatscale = int(((temp + 50.0) / 100.0) * 256)
			hex_color = '#%02x%02x%02x' % (heatscale, 128, 256 - heatscale)


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