from flask import Flask, request, abort
from pprint import pprint
import requests
import json
from webhookregister import webhookregister
from setup_room import setup_room
from setupendpoint import setup_endpoint
import os
import variables
from tabulate import tabulate
import wa_functions
import wbx_functions

app = Flask(__name__)


@app.route('/wa_receiver', methods=['POST'])
def wa_receiver():
    wa_sender = request.json['data']['sender']
    wa_url = variables.maxchat_url + "/chats/" + wa_sender + "/messages"

    auth_url = variables.db_url +'/user/check/' + wa_sender
    json_auth = json.loads(requests.get(url=auth_url).text)

    if json_auth['message'] == "user is EXIST" and wa_sender != '6287878522334':
        print('\n\n')
        pprint(request.json)
        print('\n\n')
        wa_text = request.json['data']['text'].strip()

        db_patient = variables.db_url +'/user/get'
        body = {'phoneNumber':wa_sender}
        json_patient = json.loads(requests.get(url=db_patient,json=body).text)[0]
        patient_name = json_patient['name']

        if wa_text in wa_functions.function_list():
            fwd_wa = eval("wa_functions." + wa_text + "(json_patient)")
            r_post = requests.post(url=wa_url,headers=variables.wa_header,json=fwd_wa)

        elif variables.forward[wa_sender] == True:
            fwd_wbx = {'roomId':json_patient['roomId'],'text': patient_name + ':\n' + wa_text}
            r_post = requests.post(url= variables.webex_message_url,headers=variables.bot_header,json=fwd_wbx)

        else:
            fwd_wa = {'text': "Sawadikap ibu {} :D\nSaya Mangunkusubot\nKalau mau mulai konsultasi dengan DR Wahidin. Ketik '{}'".format(patient_name,wa_functions.function_list()[0])}
            r_post = requests.post(url=wa_url,headers=variables.wa_header,json=fwd_wa)

        return 'status',r_post.status_code
        
    elif wa_sender == '6287878522334':
        print("\nIni ma mesej dari Mangunkusubot kesend to webhook, lanjut aje\n")
        abort(400)
    else:
        fwd_wa = {'text': "Maaf anda belum bisa menggunakan layanan rhamp.\nMonggo cek rhamp.io untuk info lengkap rhamp dan pendaftaran"}
        print(fwd_wa)
        #r_post = requests.post(url=wa_url,headers=variables.wa_header,json=fwd_wa)
        abort(400)

@app.route('/', methods=['GET'])
def curlcheck():
    return "masuk bro"

@app.route('/webex_to_wa', methods=['POST'])
def webex_to_wa():
    if request.method == 'POST':
        
        #cek msg yg dateng
        message_id = request.json["data"]["id"]
        
        msgdetail_url = variables.webex_message_url + '/' + message_id
        
        json_msgdetail = requests.get(url=msgdetail_url,headers=variables.bot_header).json()
        message = json_msgdetail["text"]
        sender = json_msgdetail["personEmail"]
        
        #clean the message from botname & spaces

        bot_name = json.loads(requests.get(url='https://webexapis.com/v1/people/me',headers=variables.bot_header).text)['displayName']
        message = message[len(bot_name):].strip().split(' ')
        wbx_command = message[0]
        
        #abort this route if it's a command
        if wbx_command in wbx_functions.function_list():
            print("\nAbort forwarding because this is actually a command.\n")
            abort(400)
        
        #fetch patient number
        patient_url = variables.db_url + '/user/get'
        body = {"roomId": json_msgdetail["roomId"]}
        wa_recipient = json.loads(requests.get(url=patient_url,json=body).text)[0]['phoneNumber']
        
        #actual forwarding
        
        wa_url = variables.maxchat_url + "/chats/" + wa_recipient + "/messages"
        fwd_wa = {'text': sender + " : \n"+message}
        r_post = requests.post(url=wa_url,headers=variables.wa_header,json=fwd_wa)
        return 'status',r_post.status_code
    else:
        abort(400)

@app.route('/webex_function', methods=['POST'])
def webex_function():
    
    #get the actual message
    message_id = request.json["data"]["id"] #this request is just an alert webhook, not the actual message
    msgdetail_url = variables.webex_message_url + '/'  + message_id
    json_msg = requests.get(url=msgdetail_url,headers=variables.bot_header).json()
    
    #clean the message from botname & spaces
    bot_name = json.loads(requests.get(url='https://webexapis.com/v1/people/me',headers=variables.bot_header).text)['displayName']

    message = json_msg['text'][len(bot_name):].strip().split(' ')
    wbx_command = message[0]
    try:
        cmd_argument = message[1]
    except IndexError:
        cmd_argument = ''

    if wbx_command in wbx_functions.function_list():
        r_post = eval("wbx_functions." + wbx_command + "(json_msg,cmd_argument)")
        
        return 'status',r_post.status_code
    else:
        print("\nAbort function lookup because this is actually a message.\n")
        abort(400)



if __name__ == '__main__':
    app.run(host='localhost',debug=True, use_reloader=False, port=5000)