'''
references : http://docs.python-requests.org/en/master/user/quickstart/
'''

import requests
import ast, json

print 'enter url'
url = raw_input()
print 'enter params in string format : '
payload_s = raw_input()
payload = ast.literal_eval(payload_s)
r = requests.post(url, data = json.dumps(payload), headers={"Content-Type": "application/json"})


status = r.status_code
response = r.json()
print response, status
