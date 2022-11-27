import pika, sys, os
import smtplib, ssl
from email.message import EmailMessage
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

from_email = config['gmail']['account_name']
password = config['gmail']['password']
queue_name = config['rabbit_mq']['queue_name']

def send_mail(to_email, subject, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(message)
    print(msg)
    context=ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com') as server:
            server.login(from_email, password)
            server.sendmail(from_email, to_email, msg.as_string())
            print("mail successfully sent")
        
    except smtplib.SMTPAuthenticationError:
        print('Login Failed')
        raise

def process(request):
    request_type = request['type']
    subject = 'Notification from Auction Site'
    if request_type == 'itemBid':
        message = 'Your item has been bid on.'
        send_mail(request['sellerEmail'], subject, message)
    elif request_type == 'higherBid':
        message = 'Someone has placed a higher bid on the item you had bid on.'
        for mail in request['bidderEmail']:
            send_mail(mail, subject, message)
    elif request_type == 'matchCriteria':
        message = 'An item on your watchlist appears matching your criteria.'
        send_mail(request['userEmail'], subject, message)
    else:  # endClosed
        message = 'It is 1 day before bidding ends for your item.'
        send_mail(request['sellerEmail'], subject, message)
        message = 'It is 1 day before bidding ends for the item you had bid on.'
        for mail in request['bidderEmail']:
            send_mail(mail, subject, message)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        request = json.loads(body.decode())
        process(request)

    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
