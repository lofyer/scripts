#!/usr/bin/python
from ovirtsdk.api import API
from ovirtsdk.xml import params

USERNAME = 'admin@internal'
PASSWORD = sys.argv[1]
URL = 'https://localhost/api'

if len(sys.argv) < 6:
    print "Usage: "
    print "./max-vms.py PASSWORD"
    exit(1)

api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
vms=api.vms.list()
if(len(vms)>20):
    exit(1)
