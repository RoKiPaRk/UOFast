from textwrap import indent
import requests
import uopy
import json
import UOFastDataArray

  
url = 'http://127.0.0.1:8000/UOFast'

rec =  UOFastDataArray.mrecord()
rec[0] = "10"
print("rec=",rec.json)
#rec[0,1] = "20"
mObject = UOFastDataArray.multi_svr_object(ProcessName="TEST.SUB", ProcessParams=rec)

print(mObject.json(indent=2))
#for i in range(1):
x = requests.post(url, data = mObject.json(indent=2))
if x.status_code != 200:
    print("error returned = ",x.status_code, json.loads(x.text).get("detail"))
else:
    print(x.text)

