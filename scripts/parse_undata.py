from xml.dom import minidom
import json


def getElementsByValue(self, name):
    fields = self.getElementsByTagName("field")
    for field in fields:
        if field.attributes['name'].value == name:
            if len(field.childNodes) > 0:
                return field.childNodes[0].nodeValue
            else:
                return None


minidom.Element.getElementsByValue = getElementsByValue

# Parse XML
maxes_xml = minidom.parse('UNdata_Export_20141108_183932708.xml')
mins_xml = minidom.parse('UNdata_Export_20141108_184034879.xml')

maxes_records = maxes_xml.getElementsByTagName('record')
mins_records = mins_xml.getElementsByTagName('record')

mi = 0
ma = 0
pk = 0
records_list = []
num_entries = min(len(maxes_records), len(mins_records))
print num_entries

for x in range(0, num_entries):
    max_record = maxes_records[ma]
    min_record = mins_records[mi]

    max_station_name = max_record.getElementsByValue("Station Name")
    min_station_name = min_record.getElementsByValue("Station Name")

    if max_station_name == min_station_name:
        mi += 1
        ma += 1
        pk += 1

        #wrapper = {'model': 'core.Station', 'pk': pk}

        station_number = int(
            max_record.getElementsByValue("WMO Station Number"))
        json_record = {"StationName": max_station_name,
                       "WMOStationNumber": station_number}

        # check for duplicates
        if len(records_list) > 0:
            if records_list[len(records_list)-1]["WMOStationNumber"] == station_number:
                continue

        # Need to create separate
        # put in new json record
        mins_record = {}
        maxes_record = {}

        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                  "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        for month in months:
            mins_record[month] = float(min_record.getElementsByValue(month))
            maxes_record[month] = float(max_record.getElementsByValue(month))

        json_record['mins'] = mins_record
        json_record['maxes'] = maxes_record

        #wrapper['fields'] = json_record
        # records_list.append(wrapper)
        records_list.append(json_record)
    else:
        min_country = min_record.getElementsByValue("Country or Territory")
        max_country = max_record.getElementsByValue("Country or Territory")

        if min_country == max_country:
            if min_station_name < max_station_name:
                mi += 1
            else:
                ma += 1
        elif min_country < max_country:
            mi += 1
        else:
            ma += 1

json_records = records_list
print len(records_list)

with open('data.txt', 'w') as outfile:
    json.dump(json_records, outfile)
