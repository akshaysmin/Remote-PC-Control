#!/usr/bin/env python3
#actually used modules:
import smtplib
import imaplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import sys

#importing all needed modules in advance so that its easy to run code by email:
from pprint import pprint,pformat
import email
import datetime
import os
import time
import numpy as np
from bs4 import BeautifulSoup
import requests

#default behaviour to send messages, recieved messages could be from anyone
#turn on access to less secure apps on google account of login_email
login_email  = input("Enter mail id for me : ")
login_passwd = input("Enter my password : ")
from_email = 'robocop'
to_email   = input("Enter your Email id : ")

p_index='csb11'#to identify sister bots
sleep_others=' sleepothers'
kill_switch=' kill'

class e_meta:
	msg_ids=[]
	n=1	#so that the code will only check emails after first n emails, useful for testing

def send_mail(msg_content,login_email=login_email,login_passwd=login_passwd,from_email=from_email,to_email=to_email,attachment=None):

	#Setup the MIME
	message = MIMEMultipart()
	message['From'] = from_email
	message['To'] = to_email
	message['Subject'] = 'nano response'

	part1 = MIMEText(msg_content, "plain")
	message.attach(part1)

	#The subject line

	if attachment:

		#The body and the attachments for the mail
		#message.attach(MIMEText(message))

		with open(attachment, 'rb') as f: # Open the file as binary mode

			payload = MIMEBase('application', 'octate-stream')
			payload.set_payload(f.read())
		encoders.encode_base64(payload) #encode attachment in ASCII

		#add payload header with filename
		payload.add_header("Content-Disposition","attachment; filename= {}".format(attachment))
		message.attach(payload)

	message = message.as_string()

	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	s.ehlo()

	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(login_email, login_passwd) 
	  
	# sending the mail 
	s.sendmail(from_email, to_email, message) 
	  
	# terminating the session 
	s.quit() 

def process_mailbox():
  mail = imaplib.IMAP4_SSL('imap.gmail.com')
  mail.login(login_email, login_passwd)
  mail.select('Inbox')
  rv, data = mail.search(None, "ALL")
  if rv != 'OK':
      print("No messages found!")
      return
  print(data)
  id_list=[num for num in data[0].split()[e_meta.n:] if num not in e_meta.msg_ids]
  for num in id_list:
      e_meta.msg_ids.append(num)
      rv, data = mail.fetch(num, '(RFC822)')
      if rv != 'OK':
          print("ERROR getting message", num)
          return

      msg = email.message_from_string(data[0][1].decode('utf-8'))
      subject = msg['Subject']
      print('Message %s: %s' % (num, subject))
      print('Raw Date:', msg['Date'])
      date_tuple = email.utils.parsedate_tz(msg['Date'])
      if date_tuple:
          local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
          print("Local Date:",local_date.strftime("%a, %d %b %Y %H:%M:%S"))
      return subject
  mail.close()
  mail.logout()
  return 


if __name__=='__main__':
	while True:
		time.sleep(5)
		subject=process_mailbox()
		if subject:
			try:
				if subject.startswith('Fwd:'):
					subject=subject[4:]
				elif subject.startswith('Re:'):
					subject=subject[3:]
				subject = subject.strip()
	
				if subject.startswith('#!#'):
					if subject.startswith('#!#'+'getpindex'):
						msg_send = 'program_index : {}'.format(p_index)
						send_mail(msg_send)
						print('msg_sent:\n',msg_send)
					elif not subject.startswith('#!#'+p_index) and subject.endswith(sleep_others):
						time.sleep(600)
						msg_send = '#eval time.sleep(600)'
						send_mail(msg_send)
						print('msg_sent:\n',msg_send)
					elif subject.startswith('#!#'+program_index+kill_switch):
						msg_send = 'executing senpuku ...'
						send_mail(msg_send)
						print('msg_sent:\n',msg_send)
						sys.exit()
					elif subject.startswith('#!#'+program_index):
						if subject.startswith('#attach'):
							attachment = subject[7:].strip()
							msg_send = "Here's the file you requested"
							send_mail(msg_send,attachment = attachment) 
							print('msg_sent:\n',msg_send)
						elif subject.startswith('#eval'):
							msg_send = pformat(eval(subject[5:].strip()))
							send_mail(msg_send)
							print('msg_sent:\n',msg_send)
						elif subject.startswith('#exec'):
							msg_send = pformat(exec(subject[5:].strip()))
							send_mail(msg_send)
							print('msg_sent:\n',msg_send)
						else:
							msg_send = "Command not found"
							send_mail(msg_send)
							print('msg_sent:\n',msg_send)
	
						
				elif subject.startswith('#attach'):
					attachment = subject[7:].strip()
					msg_send = "Here's the file you requested"
					send_mail(msg_send,attachment = attachment) 
					print('msg_sent:\n',msg_send)
				elif subject.startswith('#eval'):
					msg_send = pformat(eval(subject[5:].strip()))
					send_mail(msg_send)
					print('msg_sent:\n',msg_send)
				elif subject.startswith('#exec'):
					msg_send = pformat(exec(subject[5:].strip()))
					send_mail(msg_send)
					print('msg_sent:\n',msg_send)
				else:
					msg_send = "Command not found"
					send_mail(msg_send)
					print('msg_sent:\n',msg_send)
		
			except Exception as e:
				error_msg=pformat(e.__doc__)+'\n'+pformat(e.args)+'\n'+pformat(e)+'\n'
				send_mail(error_msg)
				print('error msg sent:\n',error_msg)







