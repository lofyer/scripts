#!/usr/bin/python
import socket  
  
address = ('127.0.0.1', 31500)  
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
s.bind(address)  

while True:  
	data, addr = s.recvfrom(2048)  
	print "received:", data, "from", addr  

s.close()  
