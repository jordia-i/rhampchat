import requests
import variables
import json
from pprint import pprint

users_url = variables.db_url +'/user' #+ '62859106504066'
requests.packages.urllib3.disable_warnings()
print('\nDB url : \n',users_url)

payload = {'email': 'jordia.ibrahim@packet-systems.com',
  'name': 'Jordia Ibrahim',
  'phoneNumber': '62859106504066',
  'serialNumber': 'B0:49:5F:02:8B:07'}

r_post = requests.post(url=users_url,json = payload)
print('\n\n')
print('status',r_post.status_code)
#pprint(json.loads(r_bp.text))
print('\n\n')