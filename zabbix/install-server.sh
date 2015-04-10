#!/bin/bash
yum install zabbix22-*
chkconfig zabbix-proxy on
chkconfig zabbix-server on
chkconfig zabbix-agent on
service zabbix-proxy start
service zabbix-server start
service zabbix-agent start
mysql -uroot -ppassword zabbix < /usr/share/zabbix-mysql/schema.sql
mysql -uroot -ppassword zabbix < /usr/share/zabbix-mysql/images.sql
mysql -uroot -ppassword zabbix < /usr/share/zabbix-mysql/data.sql
