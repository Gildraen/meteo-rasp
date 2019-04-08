import urllib2
import time

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText

msg = MIMEMultipart()
msg['From'] = 'gaetan.coleno@gmail.com'
msg['To'] = 'gaetan.coleno@gmail.com'
msg['Subject'] = 'Temps de réponse: {0} {1}s'.format(name, t2)
message = 'Temps de réponse: {0} - {1}'.format(t2, adresses_ip)
msg.attach(MIMEText(message))
mailserver = smtplib.SMTP('smtp.gmail.com', 587)
mailserver.ehlo()
mailserver.starttls()
mailserver.ehlo()
mailserver.login('gaetan.coleno@gmail.com', '')
mailserver.sendmail('gaetan.coleno@gmail.com', msg.as_string())
mailserver.quit();