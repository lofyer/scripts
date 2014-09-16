#!/usr/bin/env python
import pika
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='task_queue', durable=True)
print 'Waiting for message, press Ctrl+C to exit.'
def callback(ch, method, properties, body):
    print "receive message: %r" % (body,)
    time.sleep(body.count('.'))
    print "done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback, queue='task_queue')
channel.start_consuming()
