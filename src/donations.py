"""
Use imap to check for venmo/paypal email notifications of payment
"""
from imaplib2 import imaplib2
import email
import os
from time import sleep
import base64
import configparser
import logging
import sys
from threading import Thread, Event


logger = logging.getLogger('email')
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)

config = configparser.ConfigParser()
if os.path.isfile('../config/settings.ini'):
    config.read('../config/settings.ini')
else:
    logger.info("Error: no \"config/settings.ini\" file. Use \"config/settings.ini.sample\" as template.")
    exit()


global_alive = True
TEST_MODE = False
FROM_EMAIL = config.get("email", "address")
FROM_PWD = config.get("email", "password")
IMAP4_SSL_SERVER = "imap.gmail.com"
IMAP4_SSL_PORT = 993
VERBOSE = False


#####
# Idler code is from here:
#   https://gist.github.com/thomaswieland/3cac92843896040b11c4635f7bf61cfb
#####

# This is the threading object that does all the waiting on
# the event
class Idler(object):
    def __init__(self, conn, callback):
        self.thread = Thread(target=self.idle)
        self.M = conn
        self.event = Event()
        self.callback = callback

    def start(self):
        self.thread.start()

    def stop(self):
        # This is a neat trick to make thread end. Took me a
        # while to figure that one out!
        self.event.set()

    def join(self):
        self.thread.join()

    def idle(self):
        # Starting an unending loop here
        while True:
            # This is part of the trick to make the loop stop
            # when the stop() command is given
            if self.event.isSet():
                return
            self.needsync = False
            # A callback method that gets called when a new
            # email arrives. Very basic, but that's good.
            def callback(args):
                if not self.event.isSet():
                    self.needsync = True
                    self.event.set()
            # Do the actual idle call. This returns immediately,
            # since it's asynchronous.
            self.M.idle(callback=callback)
            # This waits until the event is set. The event is
            # set by the callback, when the server 'answers'
            # the idle call and the callback function gets
            # called.
            self.event.wait()
            # Because the function sets the needsync variable,
            # this helps escape the loop without doing
            # anything if the stop() is called. Kinda neat
            # solution.
            if self.needsync:
                self.event.clear()
                self.dosync()

    # The method that gets called when a new email arrives.
    # Replace it with something better.
    def dosync(self):
        logger.info('recieved changes')
        readmail_paypal(self.M, self.callback)
        readmail_venmo(self.M, self.callback)


def login():
    mail = imaplib2.IMAP4_SSL(host=IMAP4_SSL_SERVER, port=IMAP4_SSL_PORT)
    mail.login(user=FROM_EMAIL, password=FROM_PWD)
    mail.select()
    return mail


def search_venmo(mail):
    type, data = mail.search(None, '(UNSEEN FROM "venmo@venmo.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0 and VERBOSE:
        logger.info('Found {} emails'.format(mail_ids))
    return mail_ids


def readmail_venmo(mail, action=None):
    #mail = login()
    for mail_id in search_venmo(mail):
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                if VERBOSE:
                    logger.info('Subject : ' + email_subject)
                if 'paid you' in email_subject:
                    person, amount = email_subject.split(' paid you ')
                    if VERBOSE:
                        logger.info('Person: {}, Amount: {}'.format(person, amount))
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                else:
                    mail.store(mail_id, '+FLAGS', '\\SEEN')
                if VERBOSE:
                    logger.info('\n')
    # mail.close()
    # mail.logout()


def search_paypal(mail):
    type, data = mail.search(None, '(UNSEEN FROM "service@intl.paypal.com")')
    mail_ids = data[0].split()
    if len(mail_ids) > 0 and VERBOSE:
        logger.info('Found {} emails'.format(mail_ids))
    return mail_ids


def readmail_paypal(mail, action=None):
    #mail = login()
    for mail_id in search_paypal(mail):
        type, data = mail.fetch(mail_id, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                logger.info(response_part[1])
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                if VERBOSE:
                    logger.info('Subject : ' + email_subject)
                if "You've got money" in email_subject:
                    person, amount = [None, None]
                    logger.info(msg.get_payload())
                    html = base64.b64decode(msg.get_payload()).decode('utf-8')
                    if 'sent you' in html:
                        html_part = html.split(' sent you ')
                        html_part_1 = html_part[0].split('>')
                        person = html_part_1[-1]
                        html_part_2 = html_part[1].split('USD')
                        amount = html_part_2[0]
                        if VERBOSE:
                            logger.info('Person: {}, Amount: {}'.format(person, amount))
                    else:
                        if VERBOSE:
                            logger.info('WARNING: unable to parse paypal email with mail id %s' % mail_id)
                    if action:
                        action(person, amount)
                if TEST_MODE:
                    mail.store(mail_id, '-FLAGS', '\\SEEN')
                else:
                    mail.store(mail_id, '+FLAGS', '\\SEEN')
                if VERBOSE:
                    logger.info('\n')
    # mail.close()
    # mail.logout()


def thread_donations(callback):
    global global_alive
    global FROM_EMAIL

    if FROM_EMAIL == "none":
        return

    while global_alive:
        mail = login()
        idler = Idler(mail, callback)
        idler.start()
        # idler.stop()
        idler.join()
        logger.info('idler thread has joined - restarting login')
        mail.close()
        mail.logout()
        # readmail_venmo(callback)
        # sleep(5)
        # readmail_paypal(callback)
        # sleep(5)

####
# For local testing:
#     Use: $ python3 donations.py
#     Each email sent to email should print `recieved changes`
#     By default idle will timeout after 29 minutes
####


def do_something(person, amount):
    logger.info('Person: {}, Amount: {}'.format(person, amount))


if __name__ == '__main__':
    thread_donations(do_something)
