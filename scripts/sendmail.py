#!/usr/bin/python3

# Imports
import argparse
import smtplib
import sendmailConfig as config

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Parse arguments
parser = argparse.ArgumentParser(description="Sending email")

parser.add_argument("-title", "-t", dest = "msgTitle", type=str, help="email title", required=True)
parser.add_argument("-body", "-b", dest = "msgBody", type=str, help="email content", required=True)
args = parser.parse_args()

# Message data
msg = MIMEMultipart()

msg["Subject"] = args.msgTitle
msg["From"] = config.addressFrom
msg["To"] = config.addressTo
msg.attach(MIMEText(args.msgBody))

# Send mail
smtpServer = smtplib.SMTP_SSL(config.smtpServer)

smtpServer.login(config.smtpUser, config.smtpPassword)
smtpServer.sendmail(msg["From"], msg["To"], msg.as_string())
smtpServer.quit()

