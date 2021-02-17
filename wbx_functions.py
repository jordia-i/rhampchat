import variables
import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from requests_toolbelt.multipart.encoder import MultipartEncoder
import util

def getBP(json_msg_detail,duration):
    
    if duration == '':
        duration = '400'

    #fetch patient number & name
    patient_number,patient_name = util.patient_details(json_msg_detail['roomId'])

    #fetch from database
    bp_url = variables.db_url +'/bp/phn/' + patient_number + '/' + duration
    json_bp = json.loads(requests.get(url=bp_url).text)
    print('\n',json.dumps(json_bp,indent=4),'\n')

    #convert to nice Dataframe format & clean outliers
    df = pd.json_normalize(json_bp).set_index('measurementTime').drop(['telemetry.measurement.unitName','telemetry.measurement.unit'],axis=1).apply(pd.to_numeric)
    df.columns = [column.split('.')[-1] for column in df.columns.values.tolist()]
    #try:
    df = df.drop(['01/19/1970, 22:49:34','02/03/2021, 14:58:11'])
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)
    
    print(df,'\n')

    #plot Dataframe & prettify
    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(ax=ax,kind='bar')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %H:%M'))
    plt.title("{}'s historical blood pressure for the past {} hours".format(patient_name,duration))
    plt.ylabel("Blood Pressure (mmHg)")
    plt.tight_layout()

    plt.savefig('test.png')

    m = MultipartEncoder({'roomId': json_msg_detail["roomId"],
                      'files': ('test.png', open('test.png', 'rb'),'image/png')})
    
    r_post = requests.post(url=variables.webex_message_url,headers={'Authorization': 'Bearer '+variables.bot_token,
                  'Content-Type': m.content_type},data=m)
    
    return r_post

def help(json_msg_detail,arg):

    #fetch patient name
    patient_number,patient_name = util.patient_details(json_msg_detail['roomId'])

    #create text in room
    fwd = {
        'roomId': json_msg_detail["roomId"],
        'text':variables.help_text.format(patient_name,patient_name,patient_name)
    }

    r_post = requests.post(url=variables.webex_message_url,headers=variables.bot_header,data=fwd)
    return r_post

def BPanalytics(json_msg_detail,duration):

    #fetch patient name
    patient_number,patient_name = util.patient_details(json_msg_detail['roomId'])

    patient_number = '628170143313'

    #fetch from database & parse
    BPanal_url = variables.db_BPanalytics +'/hbpmanalytics/phn/' + patient_number 
    if duration != '':
        BPanal_url = BPanal_url + '/' + duration
    json_BPanal = json.loads(requests.get(url=BPanal_url).text)
    markdown = "**Patient " + patient_name + "**\n\n**Diagnosis**\n>" + json_BPanal['diagnosis'].replace('_',' ') + "\n" + \
            "- Average Systol: " + str(int(json_BPanal['hbpm']['avg_sys'])) + "\n" + \
            "- Average Diastol: " + str(int(json_BPanal['hbpm']['avg_dia'])) + "\n\n" + \
            "Quality: " + json_BPanal['quality']

    #create text in room
    fwd = {
        'roomId': json_msg_detail["roomId"],
        'markdown':markdown
    }

    r_post = requests.post(url=variables.webex_message_url,headers=variables.bot_header,data=fwd)

    return r_post


def function_list():
    l = []
    for key, value in globals().items():
        if callable(value) and value.__module__ == __name__:
            l.append(key)
            
    l.remove('function_list')
    return l