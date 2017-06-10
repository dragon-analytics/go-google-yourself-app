import boto
from boto.s3.key import Key
import subprocess

LOCAL_PATH = '/tmp/'

conn = boto.connect_s3()
bucket = conn.get_bucket('dpaequipo10')
k = Key(bucket)

k.key = 'todos_mails.mbox'
k.set_contents_from_filename(LOCAL_PATH+'todos_mails.mbox')
k.make_public()

subprocess.Popen('R CMD BATCH tasks/act_inds/ai_uptodosmails.R', shell=True)
