import sys
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from socket import *
import ssl
import base64

myEmail = 'hswkuzminash@gmail.com'
password = ''
subject = 'Smth weird'
adr = ''


def message(file):
    if file[len(file) - 3:] == "txt":
        text = open(file).read()
        part = MIMEText(text, "plain")
    elif file[len(file) - 4:] == "html":
        html = open(file).read()
        part = MIMEText(html, "html")
    else:
        jpg = open(file, "rb").read()
        part = MIMEImage(jpg)

    msg = MIMEMultipart("alternative")
    msg["From"] = myEmail
    msg["To"] = adr
    msg["Subject"] = subject

    msg.attach(part)
    return msg.as_bytes()


def send_mail(file):
    context = ssl.create_default_context()
    sock = context.wrap_socket(socket(AF_INET, SOCK_STREAM), server_hostname="smtp.gmail.com")
    sock.connect(("smtp.gmail.com", 465))
    sock.recv(2048)

    sock.send('HELO Sasha\r\n'.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 250:
        raise Exception('Bad code')

    base64_str = ("\x00" + 'hswkuzminash' + "\x00" + password).encode()
    base64_str = base64.b64encode(base64_str)
    authMsg = "AUTH PLAIN ".encode() + base64_str + "\r\n".encode()
    sock.send(authMsg)
    code = sock.recv(2048).split()[0]
    if int(code) != 235:
        raise Exception('Bad code')

    str = 'MAIL FROM: <' + myEmail + '>\r\n'
    sock.send(str.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 250:
        raise Exception('Bad code')

    str = 'RCPT TO: <' + adr + '>\r\n'
    sock.send(str.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 250:
        raise Exception('Bad code')

    sock.send('DATA\r\n'.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 354:
        raise Exception('Bad code')

    sock.send(message(file))

    sock.send('\r\n.\r\n'.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 250:
        raise Exception('Bad code')

    sock.send('QUIT\r\n'.encode('utf-8'))
    code = sock.recv(2048).split()[0]
    if int(code) != 221:
        raise Exception('Bad code')

    sock.close()


if __name__ == '__main__':
    password = sys.argv[-1]
    adr = sys.argv[-2]
    file = sys.argv[-3]

    send_mail(file)
