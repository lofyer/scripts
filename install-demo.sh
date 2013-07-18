#!/bin/bash
if [ $UID != 0 ]
then
	echo -en '\E[37;31m'"\033[1mYou need run this script as root\n\033[0m"
	exit 1
fi

echo -en '\E[37;31m'"\033[1mBefore really start, you should confirm that the\nconfiguration in \"engine-setup.answer\" is right.\n\033[0m"
echo -en '\E[37;31m'"\033[1mContinue? Y\\N\n\033[0m"
read -n 1 answer

while true
do
  case $answer in
   [yY] ) echo "continue.";break;;
   * )     exit;;
  esac
done

# Set selinux tu permissive
sed -i 's/SELINUX=enforcing/SELINUX=permissive/' /etc/selinux/config
setenforce 0
echo -en '\E[37;32m'"\033[1mSelinux configuration updated\n\033[0m"

# Enable sshd
chkconfig sshd on
service sshd start
echo -en '\E[37;32m'"\033[1mSSH service enabled\n\033[0m"
# Disable iptables
chkconfig iptables off
service iptables stop
echo -en '\E[37;32m'"\033[1mIPTABLES service disabled\n\033[0m"
# Disable firewalld
chkconfig firewalld off
service firewalld stop
echo -en '\E[37;32m'"\033[1mFIREWALLD service disabled\n\033[0m"
# Enable nfs-server
chkconfig nfs-server on
service nfs-server start
echo -en '\E[37;32m'"\033[1mNFS service enabled\n\033[0m"

PWD=$(shell pwd -P)
tar xf rpm-gerrit.tar.gz
tar xf rpm-more.tar.gz
# Using engine-setup rather than engine-setup-2
engine-setup --answer-file=engine-setup.answer
