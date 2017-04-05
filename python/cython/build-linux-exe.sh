#!/bin/bash
cython -3 --embed -o hello.c hello.py
gcc -Os -I /usr/include/python3.3m -o hello hello.c -lpython3.3m -lpthread -lm -lutil -ldl
