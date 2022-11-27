initial


## Email Inbox
- Flask app will be run on 172.20.0.9:80 to expose `/sendEmail` and `/getEmails` endpoints

**Requirements for REST server**
```bash
pip install flask
pip install imap-tools
```

**Running App**
```bash
cd /notifyService/src
python3 app.py
```
- Reference: https://github.com/ikvk/imap_tools