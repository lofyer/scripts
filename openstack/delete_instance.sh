#!/bin/bash
for i in $@
do
    mysql -uroot -ppassword << EOF
use nova;
delete from block_device_mapping where instance_uuid="$i";
delete from fixed_ips where instance_uuid="$i";
delete from instance_actions_events;
delete from instance_actions where instance_uuid="$i";
delete from instance_faults where instance_uuid="$i";
delete from instance_extra where instance_uuid="$i";
delete from instance_info_caches where instance_uuid="$i";
delete from instance_system_metadata where instance_uuid="$i";
delete from security_group_instance_association where instance_uuid="$i";
delete from virtual_interfaces where instance_uuid="$i";
EOF
