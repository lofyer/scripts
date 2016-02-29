#!/bin/bash
LIST=`pip list|gawk '{print $1}'`
for i in $LIST
do
    echo $i
    pip install --upgrade $i
done
