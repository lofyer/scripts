#!/bin/bash
ping -c 3 test.lofyer.org
if [[ $? != "0" ]]
then
	echo "Killing phddns"
	pkill phddns
	echo "Restarting phddns"
	phddns --daemon
fi
