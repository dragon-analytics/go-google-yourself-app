#!/home/ubuntu/.pyenv/shims/python
import boto
import sys, os
from boto.s3.key import Key
import subprocess
import time 

bucket='dpaequipo10'
inputfile='/indicadores/indicador_uptodosmails.csv'
conn = boto.connect_s3()
b = conn.get_bucket(bucket)
k = Key(b)
k.key = inputfile

while True:
	lista = list("indicador\n0\n")
	print(lista[10])
	while lista[10] != '1':	
		try:
			contenido = k.get_contents_as_string()
			decodificado = contenido.decode("utf-8") 
			lista = list(decodificado)
		
			print("indicador: {}, lista: {}".format(lista[10],contenido))
		except:
			lista = list("indicador\n0\n")
			lista[10]='0'
			print("algo salio mal, lista (default): {}".format("".join(lista)))

	try:
		subprocess.call(["make run"], shell=True, cwd='/home/ubuntu/dpa-equipo-10/Proyecto/pipeline')
	except:
		print("Exception al ejecutar Luigi, al parecer esta corriendo. Esperando mas tiempo")
		time.sleep(600)
	time.sleep(60)

