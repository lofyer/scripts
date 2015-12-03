#!/usr/bin/env python
from ovirtsdk.api import API
import time

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

while True:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
    vms = api.vms.list()
    print vms[0].name
    tagged_running_vms = [vm for vm in vms if vm.tags.list() != [] and vm.get_start_time() != None and vm.tags.list()[0].name == "FPGA"]
    print tagged_running_vms
    session_list = [ vm.sessions.list()[0].get_console_user() != None for vm in tagged_running_vms ]
    time.sleep(600)
    session_list_later = [ vm.sessions.list()[0].get_console_user() != None for vm in tagged_running_vms ]
    if len(session_list) != len(session_list_later):
        continue
    for i in range(len(session_list_later)):
        if session_list_later[i] == False and (session_list[i] ^ session_list_later[i]) == False:
            try:
                print "Suspend " + tagged_running_vms[i].name
                tagged_running_vms[i].suspend()
            except Exception as e:
                print e
