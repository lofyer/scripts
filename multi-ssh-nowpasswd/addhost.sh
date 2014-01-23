#!/bin/bash
if [[ $1 = "" ]]
then
	echo -e "Usage: addhost.sh"
	exit
fi
cat ~/.ssh/id_rsa.pub | ssh $1 'cat >> .ssh/authorized_keys2'
