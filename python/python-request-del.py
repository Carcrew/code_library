'''
references : http://docs.python-requests.org/en/master/user/quickstart/
'''

import requests
print 'enter url'
url = raw_input()
r = requests.delete(url, headers={"Content-Type": "application/json"})

status = r.status_code
print status
