#!/bin/bash
HARBOR_IP="172.32.3.42"
OUTPUT=$(docker images | awk 'NR>1 {print $1 ":" $2}')
for i in $OUTPUT
do
    if [[ $i == *$HARBOR_IP* ]]
    then
        echo $i
    else
        echo $i
        docker tag $i $HARBOR_IP/$i
        docker push $HARBOR_IP/$i
    fi
done
