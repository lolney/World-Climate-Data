import csv, json
from operator import itemgetter

# Parse CSV
filename = 'master-location-identifier-database-20130801.csv'

station_list = {};
with open(filename, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	coords_cols = [30,29]
	for row in spamreader:
		coords = list(row[i] for i in coords_cols)
		elevation = row[33]
		station_list[row[11]] = {'coords' : coords, 'elevation': elevation}

# Parse JSON
with open('data.txt', 'rb') as jsonfile:
	jsonobj = json.load(jsonfile);
	markers = [];
	for wrapper in jsonobj:
		record = wrapper['fields'];
		# Search coords_list for WMO Station Number
		station = station_list.get(record['WMOStationNumber'], None);
		try:
			record['coordinates'] = station['coords']
			record['elevation'] = station['elevation']
		except TypeError:
			record['coordinates'] = None
			record['elevation'] = None

	with open('data_with_coords.txt', 'w') as outfile:
		json.dump(jsonobj, outfile)