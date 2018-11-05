import smtplib
from os.path import basename
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formatdate
import html


class SendMail:
    def __init__(self, send, receiver, subject, body, files):
        self.mail = MIMEMultipart()
        self.mail['Date'] = formatdate(localtime=True)
        self.mail['Subject'] = subject
        self.mail.attach(MIMEText(html.unescape(body), 'html', 'utf-8'))

        for f in files or []:
            with open(f, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    Name=basename(f)
                )
            # After the file is closed
            part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
            self.mail.attach(part)

        self._send = send
        self._receiver = receiver

    def set_header(self, send_header=None, receiver_header=None):
        if send_header is not None:
            self.mail['From'] = Header(send_header, 'utf-8')
        if receiver_header is not None:
            self.mail['To'] = Header(receiver_header, 'utf-8')

    def send_tls_mail(self, account, password, server, port=587):
        smtp = smtplib.SMTP(server, port)
        smtp.ehlo()
        smtp.starttls()
        smtp.login(account, password)
        smtp.sendmail(self._send, self._receiver, self.mail.as_string())
        smtp.close()

    def send_mail_w_login(self, account, password, server, port=25):
        smtp = smtplib.SMTP(server, port)
        smtp.ehlo()
        smtp.login(account, password)
        smtp.sendmail(self._send, self._receiver, self.mail.as_string())
        smtp.close()

    def send_mail(self,server, port=25):
        smtp = smtplib.SMTP(server, port)
        smtp.ehlo()
        smtp.sendmail(self._send, self._receiver, self.mail.as_string())
        smtp.close()

    def send_ssl_mail(self, account, password, server, port=465):
        smtp = smtplib.SMTP_SSL(server, port)
        smtp.ehlo()
        smtp.login(account, password)
        smtp.sendmail(self._send, self._receiver, self.mail.as_string())
        smtp.close()


MAIL_FROM = 'xxxxxxxxx@gmail.com'
MAIL_TO = ['xxxxxxxxx@gmail.com']

USERNAME = 'xxxxxxxxx@gmail.com'
PASSWORD = 'sssssssssss\\n'

SUBJECT = '[TEST] report test'
BODY = '&#x3C;p&#x3E;tag p test&#x3C;/p&#x3E;&#x3C;p style=&#x27;background:black;color:white&#x27;&#x3E;tag p w/ style test&#x3C;/p&#x3E;'

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

s = SendMail(MAIL_FROM, MAIL_TO, SUBJECT, BODY, ['report_GNN5W6.pdf'])
s.send_ssl_mail(USERNAME, PASSWORD, SMTP_HOST)