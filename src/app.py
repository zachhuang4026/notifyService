from flask import Flask, request, jsonify
from imap_tools import MailBox, AND
import configparser

from receive import send_mail

app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

app.config['DEBUG'] = True

@app.route('/')
def heartbeat():
    """
    Endpoint to check if microservice is online
    """
    status_code = 200
    response = {'status_code': status_code,
                'message': 'Email REST service is online'}
    return jsonify(response), status_code

# Get emails
@app.route('/getEmails', methods=['GET'])
def get_emails():
    """
    REST endpoint to get emails sent to customer service account
    """
    emails = []
    try:
        with MailBox('imap.gmail.com').login(config['gmail']['account_name'], config['gmail']['password']) as mailbox:
            # Fetch emails with [Customer Support] in the subject
            for msg in mailbox.fetch(AND(subject="[Customer Support]")):
                email_details = {'date': msg.date, 'subject': msg.subject, 'from': msg.from_, 'to': msg.to ,'body': msg.text}
                emails.append(email_details)
        status_code = 200
        response = {'status_code': status_code, 'messages': emails}
        return jsonify(response), status_code
    
    except:
        status_code = 500
        response = {'message': 'Unable to load messages from Gmail', 'status_code': status_code}
        return jsonify(response), status_code

@app.route('/sendEmail', methods=['POST'])
def send_email():
    """
    REST endpoint to send email messages
    Input: {'to_email', 'xxx', 'subject': 'xxx', 'message': 'xxx'}
    Output: {'status_code': 'xxx', 'message': 'xxx'}
    """
    to_email = request.json.get('to_email')
    subject = request.json.get('subject')
    message = request.json.get('message')

    if None in [to_email, subject, message]:
        status_code = 400
        response = {'message': 'Bad request. Did not contain required email parameters', 'status_code': status_code}
        return jsonify(response), status_code

    try:
        send_mail(to_email, subject, message)
    except:
        status_code = 500
        response = {'message': 'Unable to send email', 'status_code': status_code}
        return jsonify(response), status_code
    
    status_code = 200
    response = {'message': 'Email successfully sent', 'status_code': status_code}
    return jsonify(response), status_code

app.run(host='0.0.0.0', port=config['rest_server']['port'])

