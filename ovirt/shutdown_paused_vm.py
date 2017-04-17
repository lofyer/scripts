#!/usr/bin/env python
#-*- coding: utf-8 -*-
from ovirtsdk.api import API
import time

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

while True:
    try:
        api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
        vms = api.vms.list()
        for vm in vms:
            if "win7" in vm.name:
                if vm.get_status().state == "paused":
                    print(vm.name)
                    vm.shutdown()
                    time.sleep(600)
    except Exception as e:
        print e
