#!/usr/bin/env python
import sys
from ovirtsdk.api import API

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)

vms = api.vms.list()

if sys.argv[1] == "start":
    for i in vms:
        if i.tags.list() != [] and i.tags.list()[0].name == "bbb" :
            i.start()

if sys.argv[1] == "stop":
    for i in vms:
        if i.tags.list() != [] and i.tags.list()[0].name == "bbb" :
            i.stop()
