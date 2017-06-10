#! /usr/bin/env python3
__author__ = 'pedrohserrano'

import sys
import os
import mailbox

if __name__ == '__main__':

	path = 'todos_mails.mbox'
	mbox = mailbox.mbox(path)

	#get mail elements
	def getstuff(message):
	    ad_from = message['From']
	    ad_cc = message['cc']
	    ad_to = message['to']
	    subj = message['Subject']
	    stuff=[str(ad_from), str(ad_cc), str(ad_to), str(subj)]
	    stuff = ''.join(stuff)
	    return stuff

	def get_mail (mbox):
		mail_stuff = []
		for message in mbox:
			#body=getbody(message)
			stuff=getstuff(message)
			mail_stuff.append(stuff)
		mail_stuff = '\n'.join(mail_stuff)

		return mail_stuff

	output = get_mail(mbox)

	f = open('mbox_messages.txt','w')
	print(output, file=f)
	
	
