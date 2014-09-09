#!/usr/bin/python2.7
import subprocess
import socket

# get client ip
a=subprocess.Popen("curl ifconfig.me",stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
postip=a.stdout.read()

address = ('localhost', 30000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(address)

data = s.recv(1024)
print "Received data is ", data

print postip
s.send(postip)

s.close()
