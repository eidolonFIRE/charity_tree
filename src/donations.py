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
from time import sleep
import base64
import configparser

config = configparser.ConfigParser()
if os.path.isfile('../config/settings.ini'):
    config.read('../config/settings.ini')
else:
    print("Error: no \"config/settings.ini\" file. Use \"config/settings.ini.sample\" as template.")
    exit()


global_alive = True
TEST_MODE = False
FROM_EMAIL = config.get("email", "address")
FROM_PWD = config.get("email", "password")
IMAP4_SSL_SERVER = "imap.gmail.com"
IMAP4_SSL_PORT = 993
VERBOSE = False


def login():
    mail = imaplib.IMAP4_SSL(host=IMAP4_SSL_SERVER, port=IMAP4_SSL_PORT)
    mail.login(user=FROM_EMAIL, password=FROM_PWD)
    mail.select()
    return mail


def search_venmo(mail):
    type, data = mail.search(None, '(UNSEEN FROM "venmo@venmo.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0 and VERBOSE:
        print('Found {} emails'.format(mail_ids))
    return mail_ids


def readmail_venmo(action=None):
    mail = login()
    for mail_id in search_venmo(mail):
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                if VERBOSE:
                    print('Subject : ' + email_subject)
                if 'paid you' in email_subject:
                    person, amount = email_subject.split(' paid you ')
                    if VERBOSE:
                        print('Person: {}, Amount: {}'.format(person, amount))
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                else:
                    mail.store(mail_id, '+FLAGS', '\\SEEN')
                if VERBOSE:
                    print('\n')
    mail.close()
    mail.logout()


def search_paypal(mail):
    type, data = mail.search(None, '(UNSEEN FROM "service@intl.paypal.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0 and VERBOSE:
        print('Found {} emails'.format(mail_ids))
    return mail_ids


def readmail_paypal(action=None):
    mail = login()
    for mail_id in search_paypal(mail):
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_bytes(response_part[1])
                email_subject = msg['subject']
                if VERBOSE:
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
                        if VERBOSE:
                            print('Person: {}, Amount: {}'.format(person, amount))
                    else:
                        if VERBOSE:
                            print('WARNING: unable to parse paypal email with mail id %s' % mail_id)
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                else:
                    mail.store(mail_id, '+FLAGS', '\\SEEN')
                if VERBOSE:
                    print('\n')
    mail.close()
    mail.logout()


def thread_donations(callback):
    global global_alive

    while global_alive:
        readmail_venmo(callback)
        sleep(5)
        readmail_paypal(callback)
        sleep(5)
