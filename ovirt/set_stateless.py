#!/usr/bin/python
USERNAME="admin@internal"
PASSWORD="admin"
URL="https://localhost/api"

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

def set_stateless(name):
    list_count = len(api.vms.list(query=name)
    for j in range(1, 21):
        vm_name = name + str(j)
        vm = api.vms.get(name=name)
        vm.set_stateless(True)
        vm.update()

set_stateless("XP-")
