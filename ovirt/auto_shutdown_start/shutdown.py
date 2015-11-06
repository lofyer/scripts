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

for j in student_vms:
    if j.name=="Win7-teacher1":
        pass
    else:
        try:
            j.stop()
        except:
            pass
