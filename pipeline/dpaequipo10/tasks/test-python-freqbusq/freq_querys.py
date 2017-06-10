#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 
from datetime import timedelta, datetime
from dateutil.parser import parse as parse_datetime
import json

import click
import boto
from boto.s3.key import Key

# Define la función para obtener las fechas, excluyendo los chats
def get_dates(data):

    datemin=datetime.now() 
    datemax=datetime.fromtimestamp(0/1e6)

    #dias = {}
    #i=0
    all_dates = []
    all_times = []
    for query in data['event']:

        query_text = query['query']['query_text']
        timestamp = int(query['query']['id'][0]['timestamp_usec'])
        dates = datetime.fromtimestamp(timestamp/1e6)
        
        date=str(dates.year)+'-'+str(dates.month)+'-'+str(dates.day)
        time=str(dates.hour)+'-'+str(dates.minute)
        #date= str(parse_datetime(timestamp/1e6)).split(' ')
        all_dates.append(date)
        all_times.append(time)

    return all_dates, all_times


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
    decodificada = contenido.decode("utf-8") 

    data = json.loads(decodificada)

    #Extrae todas las fechas y las horas
    all_dates, all_times = get_dates(data)
    date_counts = pd.Series(all_dates).value_counts().sort_index()

    date_range = pd.date_range(start=fecha_i, end=fecha_f, freq='D')
    index = date_range.map(lambda x: str(x.date()))
    date_counts = date_counts.reindex(index, fill_value=0)
    

    # Ahora se observ por mes
    all_months = [x[:-3] for x in all_dates]
    month_counts = pd.Series(all_months).value_counts().sort_index()

    date_range = pd.date_range(start=fecha_i, end=fecha_f, freq='D')
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