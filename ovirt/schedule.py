#!/usr/bin/env python
# -*- coding: utf-8 -*- 
from ovirtsdk.api import API
from ovirtsdk.xml import params
import time
import sys

if len(sys.argv) < 2:
    print "Usage: "
    print "./shutdown-scedule.py schedule.txt"
    exit(1)

USERNAME = 'admin@internal'
PASSWORD = 'admin'
URL = 'https://localhost/api'

f = open(sys.argv[1],'r')

names=[]
start_times=[]
shutdown_times=[]

for line in f.readlines():
    if line.startswith('#'):
        continue
    line = line.split()
    names.append(line[0])
    start_times.append(line[1])
    shutdown_times.append(line[2])

current_time = str(time.localtime().tm_hour) + str(time.localtime().tm_hour)

print names
print start_times
print shutdown_times

try:
    api = API(URL, username=USERNAME, password=PASSWORD, insecure=True)
except Exception as e:
    print 'Failed to login.\n%s' % str(e)
    exit(1)

# Version 1
def shutdown(name, start_time, shutdown_time):
    for i in len(names):
        list_count = len(api.vms.list(query=names[i-1]))
        for j in range(1, list_count+1):
            name = names[i-1] + str(i)
            vm = api.vms.list(query=name)
            vm.stop()

# Version 2
def shutdown(name, start_time, shutdown_time):
    for i in len(names):
        name = names[i-1] + str(i)
        for vm in api.vms.list(query=name)
            vm.stop()

def start(name, start_time, shutdown_time):

for i in range(len(names)):
    if(current_time <= start_times[i]):
        print "now shutdown."
	start(names[i], start_times[i], shutdown_times[i])
