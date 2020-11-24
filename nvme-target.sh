#!/bin/bash
modprobe nvme_tcp
modprobe nvmet
modprobe nvmet-tcp

# create target
mkdir /sys/kernel/config/nvmet/subsystems/nvmet-test
cd /sys/kernel/config/nvmet/subsystems/nvmet-test
echo 1 > attr_allow_any_host
mkdir namespaces/1
cd namespaces/1/

# option 1: use local nvme disk
echo -n /dev/nvme0n1 > device_path
echo 1 > enable

# option 2: use null device
modprobe null_blk nr_devices=1
echo -n /dev/nullb0 > device_path
echo 1 > enable

# remove target
#rmdir /sys/kernel/config/nvmet/subsystems/nvmet-test

# setup target
mkdir /sys/kernel/config/nvmet/ports/1
cd /sys/kernel/config/nvmet/ports/1
echo 10.147.27.85 > addr_traddr
echo tcp > addr_trtype
echo 4420 > addr_trsvcid
echo ipv4 > addr_adrfam
ln -s /sys/kernel/config/nvmet/subsystems/nvmet-test/ /sys/kernel/config/nvmet/ports/1/subsystems/nvmet-test

# setup client
modprobe nvme
modprobe nvme-tcp
nvme discover -t tcp -a 10.147.27.85 -s 4420
nvme connect -t tcp -a 10.147.27.85 -s 4420 -n nvmet-test
nvme list
