#!/bin/bash
yum -y install bind bind-utils
# Copy conf...

# Start services
systemctl start named
systemctl enable named
#ferewall-cmd --add-service=dns --permanent 
#firewall-cmd --reload

nmcli c modify eno16777736 ipv4.dns 192.168.0.253
nmcli c down eno16777736; nmcli c up eno16777736 

dig dns.example.com.
dig -x 192.168.0.253
