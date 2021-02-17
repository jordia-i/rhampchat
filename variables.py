from collections import defaultdict

bot_token = 'NmMwNWFmMmQtM2FmMy00OGU3LWIzYzctOWRkNGI4NmU3MGIxZDVkN2YwMjEtNGYz_PF84_8992f87e-6618-4a3c-b512-1b3b50b6f6f3'
bot_header = {"content-type":'application/json','Authorization': 'Bearer '+bot_token}

wa_token = 'CWGHXkbFBNSgWgg8kZ27sn'
wa_header = {"Content-Type":'application/json','Authorization': 'Bearer '+wa_token, "accept":"application/json"}

forward = defaultdict(lambda: False)

chats_url = 'https://daecbc96594d.ngrok.io'

maxchat_url = 'https://user.maxchat.id/rhamp/api'

db_url = 'http://rhamp-backend03.southeastasia.azurecontainer.io'

db_BPanalytics = 'http://rhamp-bp-analytics.southeastasia.azurecontainer.io:5000'

webex_message_url = 'https://webexapis.com/v1/messages'

webexwebhook_url =  "https://webexapis.com/v1/webhooks/"

webex_rooms_url = 'https://webexapis.com/v1/rooms/'

doctors_emails = [
    'ibrahimjordia@gmail.com',
    'alfa.manaf@packet-systems.com',
    'frando.manurung@packet-systems.com',
    'jordia.ibrahim@packet-systems.com'
]
"""
    'ferry.purnomo@packet-systems.com' """

help_text = "This is consulting room for patient {}\n\n\
Mention me and add a message to forward that message to {}.\nExample: @rhamp Hi {} how you doin' \n\n\
Mention me and add 'get_bp' to get his/her blood pressure reading.\nExample: @rhamp get_bp"