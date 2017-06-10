#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 
from dateutil.parser import parse as parse_datetime

import click
import boto
from boto.s3.key import Key

# Define la función para obtener las fechas, excluyendo los chats
def get_dates(mbox):
	all_dates = []
	all_times = []
	for message in mbox:
	    # it's an email and not a chat if there's no label, or if there's a label but it's not 'chat'
	    if not 'X-Gmail-Labels' in message or ('X-Gmail-Labels' in message and not 'Chat' in message['X-Gmail-Labels']):
	        if 'Date' in message and message['Date'] is not None:
	            try:
	                date, time = str(parse_datetime(message['Date'])).split(' ')
	            except Exception as e:
	                print(e, message['Date'])
	            all_dates.append(date)
	            all_times.append(time)
	        else:
	            # hangouts messages have no Date key, so skip them
	            pass
	return all_times, all_dates




@click.command()
@click.option('--bucket', type=click.Path())
@click.option('--inputfile', type=click.Path())
@click.option('--outputfile1', type=click.Path())
@click.option('--outputfile2', type=click.Path())
@click.option('--fecha_i', type=click.STRING)
@click.option('--fecha_f', type=click.STRING)
def main(bucket,inputfile,outputfile1,outputfile2,fecha_i,fecha_f):

	conn = boto.connect_s3()
	b = conn.get_bucket(bucket)
	k = Key(b)
	k.key = inputfile
	contenido = k.get_contents_as_string()

	path = '/dpaequipo10/temp_freq.mbox'
	f = open(path, 'wb')
	f.write(contenido)
	f.close()

	mbox = mailbox.mbox(path)

	#Extrae todas las fechas y las horas
	all_times, all_dates = get_dates(mbox)
	date_counts = pd.Series(all_dates).value_counts().sort_index()

	date_range = pd.date_range(start=fecha_i, end=fecha_f, freq='D')
	index = date_range.map(lambda x: str(x.date()))
	date_counts = date_counts.reindex(index, fill_value=0)

	# Ahora se observ por mes
	all_months = [x[:-3] for x in all_dates]
	month_counts = pd.Series(all_months).value_counts().sort_index()

	date_range = pd.date_range(start=fecha_f, end=fecha_f, freq='D')
	months_range = date_range.map(lambda x: str(x.date())[:-3])
	index = np.unique(months_range)
	month_counts = month_counts.reindex(index, fill_value=0)
	month_counts = pd.Series(all_months).value_counts().sort_index()

	output = date_counts.to_csv(encoding='utf-8')
	k.key = outputfile1
	k.set_contents_from_string(output)
	k.make_public()

	output = month_counts.to_csv(encoding='utf-8')
	k.key = outputfile2
	k.set_contents_from_string(output)
	k.make_public()


if __name__ == '__main__':
    main()
