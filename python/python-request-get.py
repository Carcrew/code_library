'''
references : http://docs.python-requests.org/en/master/user/quickstart/
'''

import requests
print 'enter url'
url = raw_input()
r = requests.get(url)

status = r.status_code
response = r.json()
print response, status
