import variables
from webhookregister import webhookregister
from setup_room import setup_room
import requests

def mainkan(json_patient):
    if 'roomId' not in json_patient.keys() or json_patient['roomId'] == '':
        room_id = setup_room(json_patient['name'])
        r_update_roomId = requests.post(url=variables.db_url + '/user/update/byphnum',json={"phoneNumber":json_patient['phoneNumber'], "roomId":room_id})
        webhookregister(room_id,variables.chats_url)

    variables.forward[json_patient['phoneNumber']] = True
    
    return {'text': "Sekarang tiap chat kamu akan disampaikan ke DR Wahidin."}

def function_list():
    l = []
    for key, value in globals().items():
        if callable(value) and value.__module__ == __name__:
            l.append(key)
    l.remove('function_list')
    return l