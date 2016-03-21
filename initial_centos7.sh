#!/bin/bash
#
# Script to initialize CentOS 7 for personal use.
#
yum install -y iptables-services
echo -n "DEVICE=eno16777736\nONBOOT=yes\nIPADDR=192.168.0.\nNETMASK=255.255.255.0\nGATEWAY=192.168.0.1\nDNS1=192.168.0.1" > /etc/sysconfig/network-scripts/ifcfg-eno167777736
sed -i 's/enforcing/permissive/g' /etc/selinux/config
chkconfig NetworkManager off
chkconfig firewalld off
chkconfig network on
chkconfig sshd on
iptables -F
service iptables save

echo "Now you should change your IP and reboot."
