import json
import pprint as pprint
with open('ethnicity.json') as data_file:
    ethinicty = json.load(data_file)

new_data = []

for key, value in enumerate(ethinicty):
	new_data.append({"Major" : value['Major'], "Department" : value['Department']})

with open('major.json', 'w') as outfile:
    json.dump(new_data, outfile)

pprint.pprint(new_data)