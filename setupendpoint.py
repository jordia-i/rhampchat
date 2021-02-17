import os,sys
import time
import json

def setup_endpoint():
    os.popen("pkill ngrok") # clearing previous sessions of ngrok (if any)
    os.popen("sudo ngrok http 5000 &")  # Opening Ngrok in background
    time.sleep(6) #Leaving some time to Ngrok to open
    term_output_json = os.popen('curl http://127.0.0.1:4040/api/tunnels').read()   # Getting public URL on which NGROK is listening to
    print('\n\n Term_output_json:  \n',term_output_json,'\n\n')
    tunnel_info = json.loads(term_output_json)
    public_url = tunnel_info['tunnels'][0]['public_url']
    print('\n\n Public URL:  \n',public_url,'\n\n')
    return public_url

if __name__ == '__main__':
    setup_endpoint()