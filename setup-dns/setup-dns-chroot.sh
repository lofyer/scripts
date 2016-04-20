#!/bin/bash
yum -y install bind bind-utils bind-chroot
# Copy conf...

# Start services
systemctl stop named
systemctl disable named
systemctl start named-chroot
systemctl enable named-chroot
#ferewall-cmd --add-service=dns --permanent 
#firewall-cmd --reload

dig dns.example.com.
dig -x 192.168.0.253
