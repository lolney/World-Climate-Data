import csv
import json
from operator import itemgetter

# Parse CSV
filename = 'master-location-identifier-database-20130801.csv'

station_list = {}
with open(filename, 'rb') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    coords_cols = [30, 29]
    for row in spamreader:
        try:
            coords = list(float(row[i]) for i in coords_cols)
        except ValueError:
            coords = [0, 0]
        try:
            elevation = float(row[33])
        except ValueError:
            elevation = 0
        try:
            station_num = int(row[11])
        except:
            station_num = 0
        station_list[station_num] = {'coords': coords, 'elevation': elevation}

# Parse JSON
with open('data.txt', 'rb') as jsonfile:
    jsonobj = json.load(jsonfile)
    markers = []
    for record in jsonobj:
        #record = wrapper['fields'];
        #wrapper['pk'] = '';
        # Search coords_list for WMO Station Number
        station = station_list.get(record['WMOStationNumber'], None)
        for key in record:
            if record[key] is None:
                record[key] = 'No name'
        try:
            record['coordinates'] = station['coords']
            record['elevation'] = station['elevation']
        except TypeError:
            record['coordinates'] = [0, 0]
            record['elevation'] = 0

    with open('fixtures.json', 'w') as outfile:
        json.dump(jsonobj, outfile)
