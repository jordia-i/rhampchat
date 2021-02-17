import json
import requests
import variables
from tabulate import tabulate

bp_url = 'http://20.195.52.234/' +'bp/' + '150'
requests.packages.urllib3.disable_warnings()
print('\n\nBP url : \n',bp_url)
r_bp = requests.get(url=bp_url, headers=variables.typical_header)
bp_dict = json.loads(r_bp.text)
header_table = [\
    ["Device ID ", bp_dict[0]["DeviceId"]],\
    ["User ",bp_dict[0]["User"]["Id"]],\
    ["Time Stamp ",bp_dict[0]['Telemetry']['Measurement']['TimeStamp']]]
params = list(bp_dict[0]['Telemetry']['Measurement'].keys())
measurement_table = []
for param in params:
    if param != 'TimeStamp':
        measurement_table.append([param + '  ',bp_dict[0]['Telemetry']['Measurement'][param]])

print('\n\n',tabulate(header_table))
print('\n\n',tabulate(measurement_table),'\n\n') 