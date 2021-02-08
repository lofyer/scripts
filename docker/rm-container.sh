#!/bin/bash
docker rm -f $(docker ps -qa)

CTN=$(docker ps -a|gawk '{print $1}')
for i in $CTN
do
    docker rm $i
done
