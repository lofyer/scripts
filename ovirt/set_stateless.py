#!/usr/bin/python
from ovirtsdk.api import API
from ovirtsdk.xml import params
USERNAME="admin@internal"
PASSWORD="admin"
URL="https://10.42.9.11/api"

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

def set_stateless(name):
    list_count = len(api.vms.list(query=name))
    for j in range(1, 25):
        vm_name = name + str(j)
        vm = api.vms.get(name=vm_name)
        vm.set_stateless(True)
        vm.update()
        print "Set vm %s" % vm_name

set_stateless("win7-11-")
set_stateless("win7-12-")
