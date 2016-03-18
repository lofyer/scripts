#!/usr/bin/python2.7
import socket
import os
import subprocess

address = ('localhost',30000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(5)

while True:
	ss, addr = s.accept()
	print "Connected with ", addr

	ss.send('Welcome to server')
	try:
		rc = ss.recv(1024)
		print(rc)
		output=open('postip.txt','a')
	except socket.error:
		print "Common error ignored..."
		continue
	output.write(rc)
	output.close()

ss.close()
s.close()
