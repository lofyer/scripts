#!/bin/bash

# You should change your zabbix server here.
ZABBIX_SERVER="lofyer.org"
ZABBIX_PORT="10050"

# Test linux distribution.
APT_GET="which apt-get"
echo $?
YUM="which yum"
echo $?
YUM="which ls"
echo $?
