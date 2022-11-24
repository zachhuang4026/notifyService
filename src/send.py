import pika

queue_name = 'notification_queue'

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue=queue_name)

test_email = "lleyhan08@gmail.com"
msg1 = '{\"type\":\"itemBid\", \"sellerEmail\": \"'+test_email+'\"}'
msg2 = '{\"type\":\"higherBid\", \"bidderEmail\": [\"'+test_email+'\", \"'+test_email+'\"]}'
msg3 = '{\"type\":\"matchCriteria\", \"userEmail\": \"'+test_email+'\"}'
msg4 = '{\"type\":\"endClosed\", \"sellerEmail\": \"'+test_email+'\", \"bidderEmail\": [\"'+test_email+'\", \"'+test_email+'\"]}'

for message in [msg1, msg2, msg3, msg4]:
    channel.basic_publish(exchange='', routing_key=queue_name, body=message)
    print(" [x] Sent "+message)

connection.close()
