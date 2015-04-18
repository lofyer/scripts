#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from ovirtsdk.api import API
from ovirtsdk.xml import params
import sys

if len(sys.argv) < 2:
    print "Usage: "
    print "./assign-users.py assign-users.txt"
    exit(1)

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

vms=[]
users=[]
roles=[]

try:
    f = open(sys.argv[1],'r')
except Exception as e:
    print e
    exit(1)

for line in f.readlines():
    if line.startswith('#'):
        continue
    line = line.split()
    vms.append(line[0])
    users.append(line[1])
    roles.append(line[2])

print vms
print users
print roles

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

def addpermission(vm, user, role):
        query_name = vm + "-"
        list_count = len(api.vms.list(query=query_name))
        for j in range(1, list_count+1):
            print j
            try:
                vm_name = vm + "-" + str(j)
                user_name = user + str(j)
                print "Now add %s to %s with %s" %(vm_name,user_name,role)
                user_obj = api.users.get(name=user_name)
                vm_obj = api.vms.get(name=vm_name)
                role_obj = api.roles.get(name=role)
                perm_param = params.Permission(user=user_obj,role=role_obj)
                vm_obj.permissions.add(perm_param)
            except Exception as e:
                print e
                continue

try:
    for i in range(len(vms)):
    	addpermission(vms[i-1], users[i-1], roles[i-1])
    exit(0)
except Exception as e:
    print e
