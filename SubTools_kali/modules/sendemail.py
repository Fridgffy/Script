from . import log
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import sys
import os
import datetime




def send(start, end, spend, sender, password, receiver, smtp_server, smtp_port, attachments):
	try:
		sender = sender
		password = password
		receiver = receiver
		smtp_server = smtp_server
		smtp_port = smtp_port

		msg = MIMEMultipart()
		msg['Subject'] = "subTools_kali send message"
		msg['From'] = formataddr(["subTools", sender])
		msg['To'] = formataddr(["Receiver", receiver])

		mail_body = f"[ subTools run completed ]\n\nStartTime: {start.strftime('%Y-%m-%d %H:%M:%S')}\nEndTime: {end.strftime('%Y-%m-%d %H:%M:%S')}\nSpendTime: {spend/3600} hours"
		msg.attach(MIMEText(mail_body, 'plain', 'utf-8'))

		# attachments must be a list
		if isinstance(attachments, list):
			for attachment in attachments:
				filename = os.path.split(attachment)[-1]
				with open(attachment, 'rb') as f:
					att = MIMEBase('application', 'octet-stream')
					att.set_payload(f.read())
					encoders.encode_base64(att)
					att.add_header('Content-Disposition', 'attachment', filename=filename)
					msg.attach(att)
		else:
			log.log('[ sendemail Error ] attachments must be a list')
			sys.exit(1)

		server = smtplib.SMTP_SSL(smtp_server, smtp_port)
		server.login(sender, password)
		server.sendmail(sender, [receiver,], msg.as_string())
		server.quit()
	except Exception as e:
		log.log(f"Email sending failed{e}")
		sys.exit(1)
