"""
Use imap to check for venmo email notifications of payment
Pre-req:
    create .env with:
        FROM_EMAIL=
        FROM_PWD=
Usage:
    env $(cat .env | xargs) python3 venmo.py
"""
import imaplib
import email
import os
import time
import base64

SLEEP = 0  # seconds to delay before checking email again
TEST_MODE = True  # Marks the emails as UNSEEN

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = os.environ['FROM_EMAIL'] + ORG_EMAIL
FROM_PWD = os.environ['FROM_PWD']
IMAP4_SSL_SERVER = "imap.gmail.com"
IMAP4_SSL_PORT = 993


def login():
    mail = imaplib.IMAP4_SSL(host=IMAP4_SSL_SERVER, port=IMAP4_SSL_PORT)
    mail.login(user=FROM_EMAIL, password=FROM_PWD)
    mail.select()
    return mail


def search_venmo(mail):
    type, data = mail.search(None, '(UNSEEN FROM "venmo@venmo.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0:
        print('Found {} emails'.format(mail_ids))
    return mail_ids


def filter_venmo(mail, mail_ids, action=None):
    filtered_ids = []
    for mail_id in mail_ids:
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                print('Subject : ' + email_subject)
                if 'paid you' in email_subject:
                    person, amount = email_subject.split(' paid you ')
                    print('Person: {}, Amount: {}'.format(person, amount))
                    filtered_ids.append(mail_id)
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                print('\n')

    return filtered_ids

def readmail_venmo(mail, action):
    mail_ids = search_venmo(mail)
    filtered_ids = filter_venmo(mail, mail_ids, action)
    print('Found {} venmo emails'.format(len(filtered_ids)))


def do_something(person, amount):
    print('FOUND')


def search_paypal(mail):
    type, data = mail.search(None, '(FROM "service@intl.paypal.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0:
        print('Found {} emails'.format(mail_ids))
    return mail_ids


def filter_paypal(mail, mail_ids, action=None):
    filtered_ids = []
    for mail_id in mail_ids:
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                print('Subject : ' + email_subject)
                if "You've got money" in email_subject:
                    person, amount = [None, None]
                    html = base64.b64decode(msg.get_payload()).decode('utf-8')
                    if 'sent you' in html:
                        html_part = html.split(' sent you ')
                        html_part_1 = html_part[0].split('>')
                        person = html_part_1[-1]
                        html_part_2 = html_part[1].split('USD')
                        amount = html_part_2[0]
                        print('Person: {}, Amount: {}'.format(person, amount))
                    else:
                        print('WARNING: unable to parse paypal email with mail id %s' % mail_id)
                    filtered_ids.append(mail_id)
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                print('\n')

    return filtered_ids


def readmail_paypal(mail, action):
    mail_ids = search_paypal(mail)
    filtered_ids = filter_paypal(mail, mail_ids, action)
    print('Found {} paypal emails'.format(len(filtered_ids)))


if __name__ == '__main__':
    mail = login()

    while True:
        readmail_venmo(mail, do_something)
        readmail_paypal(mail, do_something)
        time.sleep(SLEEP)
        if TEST_MODE:
            break

    mail.close()
    mail.logout()
