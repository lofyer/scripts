#!/bin/bash
BASENAME=$(basename $1 .py)
platform='unknown'
unamestr=`uname`

cython -3 --embed -o $BASENAME.c $1

if [[ "$unamestr" == 'Linux' ]]; then
    platform='linux'
    gcc -Os -I/usr/include/python3.4m -o $BASENAME $BASENAME.c -lpython3.4m -lpthread -lm -lutil -ldl
elif [[ "$unamestr" == 'FreeBSD' ]]; then
    platform='freebsd'
elif [[ "$unamestr" == 'Darwin' ]]; then
    platform='macos'
    gcc -o $BASENAME $BASENAME.c -framework Python
fi
rm -f $BASENAME.c
