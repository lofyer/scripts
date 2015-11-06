#!/usr/bin/python
from ovirtsdk.api import API
from ovirtsdk.xml import params
import time
import sys

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)

student_vms=api.vms.list(query="*")
i=0
for j in student_vms:
    if j.name=="Win7-teacher1" or j.name=="Win7-11-Base" or j.name=="Win7-12-Base":
        pass
    else:
        try:
            i+=1
            print j.name
            j.start()
        except:
            pass
    if(i%5==0):
        time.sleep(30)
