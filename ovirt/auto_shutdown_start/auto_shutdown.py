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
avail=api.storagedomains.get(name="Sys_11").get_available()/1024/1024/1024

for j in student_vms:
    if j.name=="Win7-teacher1":
        pass
    else:
        try:
            print j.name
            console_user = j.sessions.list()[0]
            if (console_user.get_console_user()!=True) and (avail <= 20):
                j.stop()
        except:
            pass
