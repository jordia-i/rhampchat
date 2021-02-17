import requests
from pprint import pprint
import json
from setup_room import setup_room
import variables

def webhookregister(roomId,public_url):

    #REGISTER FORWARDER WEBHOOK
        
    print('\nRegistering a forwarder webhook\n')

    forwarder_url = public_url +'/webex_to_wa'

    requests.packages.urllib3.disable_warnings()
    payload = {
    "targetUrl": forwarder_url,
    "resource": "messages",
    "event": "created",
    "filter": "roomId=" + roomId + "&mentionedPeople=me",
    "name": "forward to sender"
    }

    resp = requests.post(url=variables.webexwebhook_url,headers=variables.bot_header,json=payload)

    if resp.status_code != 200:
        print ('Webhook registration Error !')
        print('\n\nResponse : \n')
        pprint(json.loads(resp.text))
        print('\n\n')
        exit(0)

    print('\n\nWebhook registration success !')

    #REGISTER FUNCTION WEBHOOK
        
    print('\nRegistering a function webhook\n')
 
    function_url = public_url +'/webex_function'

    requests.packages.urllib3.disable_warnings()

    payload = {
    "targetUrl": function_url,
    "resource": "messages",
    "event": "created",
    "filter": "roomId=" + roomId + "&mentionedPeople=me",
    "name": "process functions"
    }

    resp = requests.post(url=variables.webexwebhook_url,headers=variables.bot_header,json=payload)

    if resp.status_code != 200:
        print ('Webhook registration Error !')
        print('\n\nResponse : \n')
        pprint(json.loads(resp.text))
        print('\n\n')
        exit(0)

    print('\n\nWebhook registration success !')


    #CHECK REGISTERED WEBHOOK

    print('\n\nCheck registered webhooks : \n')

    r3 = requests.get(url=variables.webexwebhook_url,headers=variables.bot_header)
    pprint(json.loads(r3.text))

if __name__ == '__main__':
    room_id = setup_room()
    #public_url = setup_endpoint()
    webhookregister(room_id,variables.public_url)