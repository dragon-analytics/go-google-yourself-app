import json
import subprocess
import codecs
import glob
#import os

LOCAL_PATH = '/tmp/'

eventos={'event':[]}
for f in glob.glob(LOCAL_PATH+"Takeout/busquedas/*.json"):
    with open(f) as data_file:
                data = json.load(data_file)
                for ev in data['event']:
                        data_event = ev
                        eventos['event'].append(data_event)

with open(LOCAL_PATH+"todas_busquedas.json", "w") as outfile:
     json.dump(eventos, outfile)