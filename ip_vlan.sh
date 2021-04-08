#!/bin/bash
ip link add link eth0 name eth0.100 type vlan id 100
ip addr add 192.168.100.1/24 brd 192.168.100.255 dev eth0.100
ip link set dev eth0.100 up
ip route add 0/0 via 192.168.100.254 dev eth0
