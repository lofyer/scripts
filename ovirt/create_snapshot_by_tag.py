#!/usr/bin/env python
import sys
from ovirtsdk.api import API
from datetime import date

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'
SNAPSHOT_NAME = 'backup-{}'.format(date.today().strftime("%Y%m%d"))

api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)

vms = api.vms.list()

for i in vms:
    if i.tags.list() != [] and i.tags.list()[0].name == sys.argv[1] :
        i.snapshots.add(params.Snapshot(description=SNAPSHOT_NAME, vm=i))
