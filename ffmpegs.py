import json
from pprint import pprint

with open('streaming.json') as f:
    data = json.load(f)

# pprint(data['streams'])
for a in data['streams']:
    pprint(a['input']+" "+a['output'])