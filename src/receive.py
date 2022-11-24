import pika, sys, os
import smtplib, ssl
from email.message import EmailMessage


def send_mail(to_email, subject, message, from_email='foursure1123@gmail.com'):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email
    msg.set_content(message)
    print(msg)
    context=ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com') as server:
            server.login(from_email, 'anhrwnearhlfaoeg')
            server.sendmail(from_email, to_email, msg.as_string())
            print("mail successfully sent")
        
    except smtplib.SMTPAuthenticationError:
        print('Login Failed')

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='notification_queue')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % body.decode())
        send_mail('lleyhan08@gmail.com', 'subject', 'content')  # test

    channel.basic_consume(queue='notification_queue', on_message_callback=callback, auto_ack=True)

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
