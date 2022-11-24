import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='notification_queue')
message = 'Hello World!'
channel.basic_publish(exchange='', routing_key='notification_queue', body=message)
print(" [x] Sent "+message)
connection.close()
