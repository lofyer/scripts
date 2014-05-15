#!/bin/bash
if [[ $1 = "" ]]
then
	echo -e "Make sure that selinux has been set to permissive or disabled.\nUsage: addhost.sh"
	exit
fi
cat ~/.ssh/id_rsa.pub | ssh $1 'cat >> .ssh/authorized_keys2; chmod 700 .ssh; chmod 640 .ssh/authorized_keys2'
