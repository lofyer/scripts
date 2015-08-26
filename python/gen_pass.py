#!/usr/bin/env python
import string
import sys
import random
import date

if len(sys.argv) <> 3:
    print("username/mail host/site password")
    exit(1)

def id_generator(size=12, chars=string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation):
    return ''.join(random.choice(chars) for _ in range(size))

f = open("password.txt","a+")
item= sys.argv[1] + " " + sys.argv[2] + " " + id_generator() + "\n"
f.write(item)
f.close()
