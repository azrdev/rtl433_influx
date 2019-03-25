#!/usr/bin/env python3
import json
from json.decoder import JSONDecodeError
from influxdb import InfluxDBClient
import sys
from datetime import datetime
import itertools


mappings = {
        'maybetemp': None,
        'temperature': None,
        'temperature_C': None,
        'temperature_C1': None,
        'temperature_C1': None,
        'temperature_2_C': None,
        'temperature_1_C': None,
        'temperature_F': None,
        'ptemperature_C': None,

        'pressure_bar': None,
        'pressure_hPa': None,
        'pressure_PSI': None,

        'humidity': None,
        'phumidity': None,
        'moisture': None,

        'windstrength': None,
        'gust': None,
        'average': None,
        'speed': None,
        'wind_gust': None,
        'wind_speed': None,

        'winddirection': None,
        'direction': None,
        'wind_direction': None,
        'wind_dir_deg': None,
        'wind_dir': None,

        'battery': None,
        'battery_mV': None,

        'rain': None,
        'rain_rate': None,
        'total_rain': None,
        'rain_total': None,
        'rainfall_accumulation': None,
        'raincounter_raw': None,

        'status': None,
        'state': None,
        'tristate': str,
        'button1': None,
        'button2': None,
        'button3': None,
        'button4': None,
        'flags': lambda x: int(str(x), base=16),
        'event': lambda x: int(str(x), base=16),
        'cmd': None,
        'cmd_id': None,
        'code': None,
        'power0': None,
        'power1': None,
        'power2': None,
        'dim_value': None,
        'depth': None,
        'depth_cm': None,
        'energy': None,
        'data': None,
        'repeat': None,
        'current': None,
        'interval': None,

        'heating': None,
        'heating_temp': None,
        'water': None,
}

client = InfluxDBClient('localhost', 8086, 'root', 'root', 'rtl433')
source = sys.stdin
if sys.argv[1:]:
    files = map(lambda name : open(name, 'r'), sys.argv[1:])
    source = itertools.chain.from_iterable(files)
for line in source:
    try:
        json_in = json.loads(line)
    except JSONDecodeError as e:
        print("error {} decoding {}".format(e, line.strip()), file=sys.stderr)
        continue

    if not 'model' in json_in:
        continue
    time = json_in.pop('time') if 'time' in json_in else datetime.now().isoformat()

    json_out = {
        'measurement': json_in.pop('model'),
        'time': time, # TODO: timezone?
        'tags': {},
        'fields': {},
    }
    for n, mapping in mappings.items():
        if n in json_in:
            mapping = mapping or (lambda x : x)
            try:
                value = json_in.pop(n)
                json_out['fields'][n] = mapping(value)
            except Exception as e:
                print('error {} mapping {}'.format(e, value))
                continue
    json_out['tags'] = json_in # the remainder

    if not len(json_out['fields']):
        continue # invalid: we have no data #TODO: notify about error

    try:
        client.write_points([json_out])
    except Exception as e:
        print("error {} writing {}".format(e, json_out), file=sys.stderr)

