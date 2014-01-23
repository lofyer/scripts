#!/bin/bash
if [[ $1 = "" ]] 
then
    echo -e "Usage: cmd.sh"
	exit
fi

declare -a HOSTS=($(cat hosts.list))
cnt=${#HOSTS[@]}

for ((i=0;i<cnt;i++)); do
    ssh ${HOSTS[i]} '$1'
done
