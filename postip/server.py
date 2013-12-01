#!/usr/bin/python2.7
import socket
import os
import subprocess

address = ('lofyer.org',30000)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(address)
s.listen(5)

while 1:
	ss, addr = s.accept()
	print "Connected with ", addr

	ss.send('Welcome to server')
	try:
		rc = ss.recv(1024)
		output=open('postip.txt','a')
	except socket.error:
		print "Common error ignored..."
		continue
	print(rc)
	output.write(rc)
	output.close()

ss.close()
s.close()
