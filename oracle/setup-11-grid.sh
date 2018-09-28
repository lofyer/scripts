#!/bin/bash
wget http://172.20.11.101/sda/o11g/linux.x64_11gR2_database_1of2.zip
wget http://172.20.11.101/sda/o11g/linux.x64_11gR2_database_2of2.zip

#unzip

hostnamectl set-hostname rac1-pub
#hostnamectl set-hostname rac2-pub
nmcli d connect eth1

sed -i 's/^SELINUX=*$/SELINUX=disabled/g' /etc/selinux/config
setenforce 0

yum install -y gcc libaio glibc compat-libstdc++ gcc-c++ libaio-devel unixODBC unixODBC-devel pdksh oracle-rdbms-server-11gR2-preinstall oracleasm oracleasm-support 

oracleasm configure -e -s y -u oracle -g oinstall

mkdir -p  /u01
chown -R oracle:oinstall /u01
chmod -R 775 /u01/

cat << EOF >> /etc/hosts
172.20.14.252 rac1-pub
172.20.14.246 rac2-pub

192.168.3.153 rac1-pri
192.168.4.104 rac2-pri

172.20.14.201 rac1-vip
172.20.14.202 rac2-vip

172.20.14.211 rac-scan
172.20.14.212 rac-scan
172.20.14.213 rac-scan
EOF

rpm -Uvh rpm/cvuqdisk*

parted /dev/sda mklabel gpt
parted /dev/sda mkpart primary 2048s 100%

oracleasm createdisk DISK1 /dev/sda1
oracleasm scandisks

gridInstaller setup ssh with oracle or other users

./runInstaller
