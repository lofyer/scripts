#!/usr/bin/python
import socket

address = ('127.0.0.1', 31500)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
	msg = raw_input()
	s.sendto(msg, address)
	
s.close()
