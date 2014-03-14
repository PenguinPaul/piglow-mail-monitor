import imaplib
import time
import getpass
import email
import socket
from email.parser import HeaderParser
from piglow import PiGlow

piglow = PiGlow()

def setup():
    global TTS
    global PARSER
    global IMAP_SERVER
    global MAIL_SERVERS

    IMAP_SERVER = None

    MAIL_SERVERS = {'gmail.com': {'Server': str(socket.gethostbyname('imap.gmail.com'))},
                    'yahoo.com': {'Server': str(socket.gethostbyname('imap.mail.yahoo.com'))},
                    'aol.com': {'Server': str(socket.gethostbyname('imap.aol.com'))}}


def getLogin():
    username = raw_input("Email address: ")
    password = getpass.getpass()
    return username, password

def getMessages(server):
    server.select()
    _, data = server.search(None, 'All')
    return data[0].split()


def main():

    setup()
    global PARSER
    global IMAP_SERVER
    global MAIL_SERVERS

    print("Please enter in your email account details.")
    username, password = getLogin()
    username2 = username.split("@")
    while len(username2) != 2:
        print("Please enter a valid email address.")
        username, password = getLogin()
        username2 = username.split("@")

    if username2[1] not in MAIL_SERVERS:
        raise NotImplementedError("Support for your email provider has not been implemented yet")

    IMAP_SERVER = imaplib.IMAP4_SSL(MAIL_SERVERS[username2[1]]["Server"], MAIL_SERVERS[username2[1]].get("Port", 993))
    IMAP_SERVER.login(username, password)

    read = []

    while True:
	typ, data = IMAP_SERVER.select('Inbox', 1)
	typ, data = IMAP_SERVER.search(None, 'NEW')
        new_messages = len(data[0].split())
	if new_messages > 0:
		piglow.led5(5)
	else:
		piglow.led5(0)
        time.sleep(1)

if __name__ == "__main__":
    main()
