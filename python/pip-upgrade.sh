#!/bin/bash
PIP_CMD=pip2
LIST=`$PIP_CMD list|gawk '{print $1}'`
for i in $LIST
do
    echo $i
    $PIP_CMD install --upgrade $i
done
