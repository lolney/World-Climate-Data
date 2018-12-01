import json
import sqlite3

def flatten(item, name):
	out = []
	if type(item[1]) == type({}):
		for entry in item[1].items():
			out = out + flatten(entry, item[0] + '_' + name);
	elif type(item[1]) == type([]):
		for i, entry in enumerate(item[1]):
			a = tuple([item[0] + name + '_' + str(i), entry]);
			out.append(a);
	else:
		item = tuple([name + item[0], item[1]]);
		out.append(item);
	return out

JSON_FILE = "World_Climate_Data/core/data_with_coords.txt"
DB_FILE = "World_Climate_Data/db.sqlite3"
 
traffic = json.load(open(JSON_FILE))
conn = sqlite3.connect(DB_FILE)
  
data = traffic['records']
formatted_data = [];
keys = []
keys_orig = []

for dictionary in data:
	new_dict = {};
	for item in dictionary.items():
		new_dict = dict(new_dict.items() + flatten(item, ''));
	formatted_data.append(new_dict);
	print new_dict
data = formatted_data;

for key in data[0]:
	keys.append(''.join(key.split()))
	keys_orig.append(key)

c = conn.cursor()
c.execute('drop table minmax');
c.execute('create table minmax (' + ', '.join(keys) + ')');
c.close

query = "insert into minmax ({0}) values (?{1})"
query = query.format(", ".join(keys), ",?" * (len(keys) - 1))
print query

for record in data:
	c = conn.cursor()
	result = tuple(record.get(c) for c in keys_orig)
	print result
	c.execute(query, result)
	c.close
 
conn.commit()
conn.close()
