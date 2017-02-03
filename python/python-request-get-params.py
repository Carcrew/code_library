'''
references : http://docs.python-requests.org/en/master/user/quickstart/
'''

import requests
import ast

print 'enter url'
url = raw_input()
print 'enter params in string format : '
payload_s = raw_input()
payload = ast.literal_eval(payload_s)
r = requests.get(url, params=payload)


status = r.status_code
response = r.json()
print response, status
