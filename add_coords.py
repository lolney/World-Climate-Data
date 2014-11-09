import csv, json
from operator import itemgetter

# Parse CSV
filename = 'master-location-identifier-database-20130801.csv'

coords_list = {};
with open(filename, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	coords_cols = [30,29]
	for row in spamreader:
		coords_list[row[11]] = list(row[i] for i in coords_cols)

# Parse JSON
with open('data.txt', 'rb') as jsonfile:
	jsonobj = json.load(jsonfile);
	markers = [];
	for record in jsonobj['records']:
		# Search coords_list for WMO Station Number
		coords = coords_list.get(record['WMO Station Number'], None);
		record['coordinates'] = coords

	with open('data_with_coords.txt', 'w') as outfile:
		json.dump(jsonobj, outfile)