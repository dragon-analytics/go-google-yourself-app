import boto
from boto.s3.key import Key
import subprocess

#print os.listdir('/tmp/')
conn = boto.connect_s3()
bucket = conn.get_bucket('dpaequipo10')
k = Key(bucket)


k2 = Key(bucket)
k2.key = 'indicadores/indicador_uptodosmails.csv'
k2.set_contents_from_filename('/tmp/indicador_uptodosmails.csv')
k2.make_public()
