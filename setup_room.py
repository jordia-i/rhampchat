import requests
import json
import variables
from pprint import pprint

def setup_room(patient_name):


    #CREATE NEW ROOM

    data = {'title': patient_name + ' consulting'}
    r_create_room = requests.post(url=variables.webex_rooms_url,headers=variables.bot_header,data=json.dumps(data))
    newroomId = r_create_room.json()['id']
    print('\n\nNew room created : \n',newroomId)
        
    webex_member_url = 'https://webexapis.com/v1/memberships/'
    for i in variables.doctors_emails:
        data = {
            'roomId': newroomId,
            'personEmail': i,
            'isModerator': 'false'            
        }
        r_add_member = requests.post(url=webex_member_url,headers=variables.bot_header,data=json.dumps(data))

    webex_message_url = 'https://webexapis.com/v1/messages/'
    fwd = {
        'roomId': newroomId,
        'text':variables.help_text.format(patient_name,patient_name,patient_name)
    }
    
    r_post = requests.post(url= webex_message_url,headers=variables.bot_header,json=fwd)

    return newroomId

if __name__ == '__main__':
    setup_room()