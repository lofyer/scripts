#!/bin/bash
for i in `seq 1 20`
do
    ./addldapuser.sh user$i
done
