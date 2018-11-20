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


def search(mail):
    type, data = mail.search(None, '(UNSEEN FROM "venmo@venmo.com")')
    mail_ids = data[0].split()
    print('Found {} emails'.format(mail_ids))
    return mail_ids


def filter(mail, mail_ids, action=None):
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
                    if TEST_MODE:
                        mail.store(mail_id, '-FLAGS', '\\SEEN')
                    if action:
                        action(person, amount)
                print('\n')

    return filtered_ids


def do_something(person, amount):
    print('FOUND')


def readmail(mail):
    mail_ids = search(mail)
    filtered_ids = filter(mail, mail_ids, do_something)
    print('Found {} emails'.format(len(filtered_ids)))


if __name__ == '__main__':
    mail = login()

    while True:
        readmail(mail)
        time.sleep(SLEEP)

    mail.close()
    mail.logout()
