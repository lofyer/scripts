#!/bin/bash
BASENAME=$(basename $1 .py)
cython -2 --embed -o $BASENAME.c $1
gcc -o $BASENAME $BASENAME.c -framework Python
rm -f $BASENAME.c
#gcc -Os -I /usr/include/python3.3m -o hello hello.c -lpython3.3m -lpthread -lm -lutil -ldl
