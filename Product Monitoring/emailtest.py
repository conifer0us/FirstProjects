import smtplib
from email.mime.text import MIMEText

email = None
password = None
sent_from = email
to = None
body = None

subject = 'CHECK GRAPHICS CARD LISTING'
msg = MIMEText(body)
msg['Subject'] = subject
msg['From'] = sent_from
msg['To'] = to

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(email,password)
server.sendmail(sent_from, to, msg.as_string())
server.close()
