#!/usr/bin/env python
import os
import psutil
import requests
import time
from datetime import datetime

#
# Get current data
#

URI = "http://192.168.0.67:8000"
URL_SCH = URI + "/virtdesk/schedule/request/"
URL_DSK = URI + "/virtdesk/tag/getdesktops/"
# Start VM_WINDOW vms every VM_SLICE seconds
VM_WINDOW = 5
VM_SLICE = 0
# Time between classes in minute
FREE_TIME = 0

current_time = datetime.today()

sch_data = requests.post(URL_SCH).json()
sch_msg = sch_data['message']
print sch_msg

cstime_list = list()
cetime_list = list()
class_list = list()
class_vms_list = dict()

# Do I need sort the lists by cstime?
for i in range(len(sch_msg)):
    cs_p = datetime.strptime(sch_msg[i]['cstime'], '%I:%M %p')
    ce_p = datetime.strptime(sch_msg[i]['cetime'], '%I:%M %p')
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
IN_SCHEDULE = 'no'
f_name = "/tmp/tmp_in_schedule"
print "PID:"
CURRENT_PID = psutil.os.getpid()
print CURRENT_PID
PROCESS = psutil.Process(CURRENT_PID).as_dict()
print PROCESS['pid'], PROCESS['cmdline']
try:
    f = file(f_name, 'r')
    IN_SCHEDULE = f.readline().strip()
    f.close()
except Exception as e:
    print e
print "In schedule?"
print IN_SCHEDULE

if IN_SCHEDULE == 'no':
    f = file(f_name, 'w')
    f.write('yes')
    f.close()
    for i in range(len(class_list)):
        print "In class"
        print class_list[i]
        print cstime_list[i].hour
        print cstime_list[i].minute
        if current_time.hour != cstime_list[i].hour and current_time.minute != cstime_list[i].minute:
            for j in range(len(class_vms_list[class_list[i]])):
                # If we are in a schedule process, we will stop
                print "Starting vm..."
                print class_vms_list[class_list[i]][j]
                # Start vm
                # requests.
                if j != 0 and j%VM_WINDOW == 0:
                    time.sleep(VM_SLICE)
                pass
        # Test sleep
        time.sleep(5)
    f = file(f_name, 'w')
    f.write('no')
    f.close()

    # If (cs_time of next class - ce_time of this class) is less than FREE_TIME and both classes are same, we will not shutdown the vm

if (i+1) != len(class_list) and class_list[i] == class_list[i+1] and ((cstime_list[i+1] - ce_time_list[i]) + (cstime_list[i+1] - cstime_list[i])*60) <= FREE_TIME :
    pass
elif current_time.hour == cetime_list[i].hour and current_time.minute == cetime_list[i].minute:
    for j in len(range(class_vms_list[i])):
        # Stop vm
        pass
