import requests
import variables
import json

def patient_details(room_id):
    patient_url = variables.db_url + '/user/get'
    body = {"roomId": room_id}
    json_patient = json.loads(requests.get(url=patient_url,json=body).text)[0]
    return json_patient['phoneNumber'],json_patient['name']
