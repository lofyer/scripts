#!/usr/bin/env python
import os
import psutil
import requests
import time
from datetime import datetime

#
# Get current data
#

BIN='sch.py'
URI = "http://192.168.0.238"
URL_SCH = URI + "/virtdesk/schedule/request/"
URL_DSK = URI + "/virtdesk/tag/getdesktops/"
URL_START = URI + "/virtdesk/desktop/start?instant=True&vm_id="
URL_SHUTDOWN = URI + "/virtdesk/desktop/shutdown?instant=True&vm_id="
# Start VM_WINDOW vms every VM_SLICE seconds
VM_WINDOW = 5
VM_SLICE = 10
# We will start vms before and after start_time about STARTING_TIME minutes
STARTING_TIME = 20
# Time between classes in minute
QUOTA_TIME = 10

current_time = datetime.today()

sch_data = requests.post(URL_SCH).json()
sch_msg = sch_data['message']
print sch_msg

cstime_list = list()
cetime_list = list()
class_list = list()
class_vms_list = dict()
if(len(sch_msg) == 0):
    exit(0)
# Do I need sort the lists by cstime?
for i in range(len(sch_msg)):
    print sch_msg[i]
    cs_p = datetime.strptime(sch_msg[i]['cstime'], '%H:%M')
    ce_p = datetime.strptime(sch_msg[i]['cetime'], '%H:%M')
    #cs_p = datetime.strptime(sch_msg[i]['cstime'], '%I:%M %p')
    #ce_p = datetime.strptime(sch_msg[i]['cetime'], '%I:%M %p')
    #cstime_list.append(cs_p.strftime('%H:%M'))
    #cetime_list.append(ce_p.strftime('%H:%M'))
    cstime_list.append(cs_p)
    cetime_list.append(ce_p)
    class_list.append(sch_msg[i]['lname'])
    # Show vm
    vm_list = list()
    payload = {'tag_name':sch_msg[i]['lname']}
    # Add vm to sch_msg
    if class_vms_list.has_key(sch_msg[i]['lname']) == False :
        msg_data = requests.get(URL_DSK, params=payload).json()['message']
        print "msg_data"
        print msg_data
        for j in range(len(msg_data)):
            vm_list.append(msg_data[j]['id'])
        class_vms_list.update({sch_msg[i]['lname']:vm_list})

print "cstime"
print cstime_list
print "cetime"
print cetime_list
print "class"
print class_list
print "class_vms"
print class_vms_list

#
# Schdule to start and shutdown
#

# If we had IN_SCHEDULE = 'yes' we won't proceed to start, we must check if this process is dead or not to reset IN_SCHEDULE
IN_SCHEDULE = 0
for p in psutil.process_iter():
    if p.as_dict()['cmdline'] != None :
        if any('sch.py' in s for s in p.as_dict()['cmdline']):
            IN_SCHEDULE += 1
            print p.as_dict()['cmdline']
print "In schedule?"
print IN_SCHEDULE

if IN_SCHEDULE == 1:
    for i in range(len(class_list)):
        print "In class"
        print class_list[i]
        print cstime_list[i].hour
        print cstime_list[i].minute
        print "STARTING_TIME"
        print abs((cstime_list[i].hour - current_time.hour)*60 +  (cstime_list[i].minute - current_time.minute ))
        if abs((cstime_list[i].hour - current_time.hour)*60 +  (cstime_list[i].minute - current_time.minute )) <= STARTING_TIME :
            for j in range(len(class_vms_list[class_list[i]])):
                # If we are in a schedule process, we will stop
                print "Starting vm..."
                #print class_vms_list[class_list[i]][j]
                # Start vm
                temp_url = URL_START + class_vms_list[class_list[i]][j]
                print temp_url
                requests.get(temp_url)
                if j != 0 and j%VM_WINDOW == 0:
                    time.sleep(VM_SLICE)
                pass
    # If (cs_time of next class - ce_time of this class) is less than QUOTA_TIME and both classes are same, we will not shutdown the vm

if (i+1) != len(class_list) and class_list[i] == class_list[i+1] and ((cstime_list[i+1] - ce_time_list[i]) + (cstime_list[i+1] - cstime_list[i])*60) <= QUOTA_TIME:
    pass
elif current_time.hour == cetime_list[i].hour and current_time.minute == cetime_list[i].minute:
    for j in range(len(class_vms_list[class_list[i]])):
        # Stop vm
        temp_url = URL_SHUTDOWN + class_vms_list[class_list[i]][j]
        print temp_url
        requests.get(temp_url)
        pass
