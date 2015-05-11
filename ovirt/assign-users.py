#!/usr/bin/env python
# -*- coding: utf-8 -*- 

from ovirtsdk.api import API
from ovirtsdk.xml import params
import sys

if len(sys.argv) < 3:
    print "Usage: "
    print "./assign-users.py admin_password assign-users.csv"
    exit(1)

USERNAME = 'admin@internal'
PASSWORD = sys.argv[1]
URL = 'https://localhost/api'

vms=[]
users=[]
roles=[]

try:
    f = open(sys.argv[2],'r')
except Exception as e:
    print e
    exit(1)

for line in f.readlines():
    if line.startswith('#'):
        continue
    line = line.split()
    vms.append(line[0])
    users.append(line[1])
    roles.append(line[2:])

print vms
print users
print roles

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

def addpermission(vm, user, role):
    for rol in role:
    	try:
            print "Now add %s to %s with %s" %(vm,user,rol)
            user_obj = api.users.get(name=user)
            vm_obj = api.vms.get(name=vm)
            rol_obj = api.roles.get(name=rol)
            perm_param = params.Permission(user=user_obj,role=rol_obj)
            vm_obj.permissions.add(perm_param)
    	except Exception as e:
       	    print e
            continue

try:
    for i in range(len(vms)+1):
    	addpermission(vms[i-1], users[i-1], roles[i-1])
    exit(0)
except Exception as e:
    print e
    exit(1)
