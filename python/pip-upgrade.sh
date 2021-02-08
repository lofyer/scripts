#!/bin/bash
PIP_CMD=pip3.9
LIST=`$PIP_CMD list|gawk 'NR>2 {print $1}'`
for i in $LIST
do
    echo $i
    $PIP_CMD install --upgrade $i
done
