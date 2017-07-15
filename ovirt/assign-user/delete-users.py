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
URL = 'https://localhost/ovirt-engine/api'

vms=[]

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

print vms

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

def delete_permission(vm):
    try:
        vm_obj = api.vms.get(name=vm)
        perm_obj = vm_obj.get_permissions().list()
        for i in perm_obj:
            try:
                i.delete()
    	    except Exception as e:
       	        print e
    except Exception as e:
        print e

try:
    for i in range(len(vms)):
    	delete_permission(vms[i-1])
    exit(0)
except Exception as e:
    print e
    exit(1)
