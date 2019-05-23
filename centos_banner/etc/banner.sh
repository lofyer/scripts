#!/bin/bash
ip=$(ifconfig eth0| awk '/inet / {print $2}' | cut -f2 -d:)
if [[ $? = 0 && $ip != "" ]]; then
    echo "OK"
    sed "s/THIS_HOST_IP/$ip/" /etc/banner.txt > /etc/issue
    sed "s/THIS_HOST_IP/$ip/" /etc/banner.txt > /etc/ssh/banner
else
    cat /etc/banner.txt > /etc/issue
    cat /etc/banner.txt > /etc/ssh/banner
fi
