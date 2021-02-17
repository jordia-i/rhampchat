
import requests
from pprint import pprint
import json
from setup_room import setup_room
import variables

def check_bot_rooms():
    resp = requests.get(url=variables.webex_rooms_url,headers=variables.bot_header)

    resp_json = json.loads(resp.text)
    list_rooms = [n for n in resp_json['items'] if n['type'] =='group']

    print('\n\nExisting rooms : \n')
    pprint(list_rooms)

    return list_rooms

requests.packages.urllib3.disable_warnings()


#CLEAR EXISTING WEBHOOK

resp = requests.get(url=variables.webexwebhook_url,headers=variables.bot_header)

resp_json = json.loads(resp.text)
print('\n\nClearing registered webhooks : \n')
pprint(resp_json)

for i in resp_json['items']:
    deleting_url = variables.webexwebhook_url + i['id']
    r = requests.delete(url=deleting_url,headers=variables.bot_header)
    print('\n\n Deleting webhook ID ',i['id'],'\nStatus : ',r,'\n')


#CLEAN EXISTING ROOMS

list_rooms = check_bot_rooms()
print('\n\nClearing Existing rooms : \n')
for room in list_rooms:
    
    #delete from webex
    deleting_wbx_url = variables.webex_rooms_url + room['id']
    r_wbx = requests.delete(url=deleting_wbx_url,headers=variables.bot_header)

    #delete from rhamp db
    patient_url = variables.db_url + '/user/get'
    body = {"roomId": room['id']}
    patient_number = json.loads(requests.get(url=patient_url,json=body).text)[0]['phoneNumber']

    print(['\nPatient number: ',patient_number,"\n"])
    
    deleting_db_url = variables.db_url + '/user/update/byphnum'
    delete_body = {"phoneNumber":patient_number, "roomId":''}
    r_db = requests.post(url=deleting_db_url,json=delete_body)
    print('\n\n Deleting room ',room['title'],'\nStatus webex: ',r_wbx,'\nStatus DB: ',r_db)

#delete from rhamp db
"""patient_url = variables.db_url + '/user/get'
body = {"roomId": room['id']}
patient_number = json.loads(requests.get(url=patient_url,json=body).text)[0]['phoneNumber']"""

patient_number = '62859106504066'

print(['\nPatient number: ',patient_number,"\n"])

deleting_db_url = variables.db_url + '/user/update/byphnum'
delete_body = {"phoneNumber":patient_number, "roomId":''}
r_db = requests.post(url=deleting_db_url,json=delete_body)
print('\n\n Deleting room ','\nStatus DB: ',r_db)