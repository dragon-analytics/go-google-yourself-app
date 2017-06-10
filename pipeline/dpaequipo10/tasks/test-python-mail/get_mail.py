__author__ = 'pedrohserrano'

import sys
import os
import mailbox
from email import header
import codecs
import click
import boto
from boto.s3.key import Key

@click.command()
@click.option('--bucket', type=click.Path())
@click.option('--inputfile', type=click.Path())
@click.option('--outputfile', type=click.Path())
def main(bucket,inputfile,outputfile):

	conn = boto.connect_s3()
	b = conn.get_bucket(bucket)
	k = Key(b)
	k.key = inputfile
	contenido = k.get_contents_as_string()

	path = '/dpaequipo10/temp.mbox'
	f = open(path, 'wb')
	f.write(contenido)
	f.close()
	
	objmbox = mailbox.mbox(path)
	
	#get mail elements
	def getstuff(message):
		ad_from = message['From']
		ad_cc = message['cc']
		ad_to = message['to']
		subj = message['Subject']
		#id_msg = message["Message-ID"]
		#subj = re.sub(r"(=\?.*\?=)(?!$)", r"\1 ", msg['Subject'])
		if isinstance(subj, str):
			subj = header.decode_header(subj)
		else:
			subj = ""
		#subj=subj.encode('utf-8')
		#decoded = base64.b64decode(msg['Subject'])
		#decode the utf-8
		#subj = str(decoded, 'latin-1')
		stuff=[str(ad_from), str(ad_cc), str(ad_to), str(subj)]
		stuff = ''.join(stuff)
		#stuff=subj
		return stuff

	def get_mail (mbox):
		mail_stuff = []
		for omessage in mbox:
			stuff=getstuff(omessage)
			mail_stuff.append(stuff)
		mail_stuff = '\n'.join(mail_stuff)
		return mail_stuff

	output = get_mail(objmbox)

	k.key = outputfile
	k.set_contents_from_string(output)
	k.make_public()

	
if __name__ == '__main__':
	main()
