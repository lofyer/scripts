#!/bin/bash
if [[ $1 = "" ]] 
then
    echo -e "Usage: cmd.sh 'cmd1;cmd2;...'"
	exit
fi

declare -a HOSTS=($(cat hosts.list))
cnt=${#HOSTS[@]}

for ((i=0;i<cnt;i++)); do
    echo -en "${HOSTS[i]}\n$@\n"
    ssh ${HOSTS[i]} $@
done
