#!/bin/bash
declare -a HOSTS=($(cat hosts.list))
cnt=${#HOSTS[@]}

for ((i=0;i<cnt;i++)); do
	cat script | ssh ${HOSTS[i]} 'bash'
done
