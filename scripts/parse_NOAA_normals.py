import csv
import json


def parseMonthly(path):
    stations = []
    with open(path, 'r') as datafile:

        for row in datafile:
            row = row.split()
            stationID = row[0]
            nums = [float(a[0:len(a)-1]) / 10 for a in row[1:13]]
            nums = map(lambda x: (x - 32) * 5 / 9, nums)
            nums = map(lambda x: round(x, 1), nums)

            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                      "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            months_record = {}

            for i, m in enumerate(months):
                months_record[m] = nums[i]

            stations.append(months_record)

    return stations


def parseInfo(path):
    info = []
    with open(path, 'r') as datafile:

        for row in datafile:
            row = row.split()
            try:
                row.remove('TRADITIONAL')
            except ValueError:
                pass
            try:
                row.remove('PSEUDONORMALS')
            except ValueError:
                pass
            try:
                row.remove('GSN')
            except ValueError:
                pass
            try:
                row.remove('HCN')
            except ValueError:
                pass
            try:
                if int(row[-1]) > 1000:
                    row.pop(-1)
            except ValueError:
                pass

            di = {
                'coordinates': [float(row[2]), float(row[1])],
                'elevation': float(row[3]),
                'StationName': " ".join(row[5:]),
                'WMOStationNumber': 0
            }

            info.append(di)

    return info


maxes = parseMonthly('rawdata/mly-tmax-normal.txt')
mins = parseMonthly('rawdata/mly-tmin-normal.txt')
info = parseInfo('rawdata/temp-inventory.txt')
for i, entry in enumerate(info):
    entry['mins'] = mins[i]
    entry['maxes'] = maxes[i]

with open('NOAAfixtures.json', 'w') as outfile:
    json.dump(info, outfile)
