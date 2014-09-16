#!/usr/bin/env python
import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.exchange_declare(exchange='logs',exchange_type='fanout')
message = ' '.join(sys.argv[1:]) or "[ INFO ]: Hello world."
channel.basic_publish(exchange='logs',routing_key='',body=message)
print "send %r" %(message,)
connection.close()
