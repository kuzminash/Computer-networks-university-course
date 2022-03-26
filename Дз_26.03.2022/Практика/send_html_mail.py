import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from bs4 import BeautifulSoup as bs
myEmail = 'hswkuzminash@gmail.com'
password = ''
subject = 'Smth weird'

def send_mail(TO, msg):
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(myEmail, password)
    server.sendmail(myEmail, TO, msg.as_string())
    server.quit()

if __name__ == '__main__':
    password = sys.argv[-1]
    adr = sys.argv[-2]
    html = open("letter.html").read()
    html_part = MIMEText(html, "html")
    msg = MIMEMultipart("alternative")
    msg["From"] = myEmail
    msg["To"] = adr
    msg["Subject"] = subject

    msg.attach(html_part)
    send_mail(adr, msg)



