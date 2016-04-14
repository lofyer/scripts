#!/bin/bash
CTN=$(docker ps -a|gawk '{print $1}')
for i in $CTN
do
    docker rm $i
done
