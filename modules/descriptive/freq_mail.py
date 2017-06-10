#! /usr/bin/env python3

import sys
import os
import operator
import mailbox
import pandas as pd
import numpy as np 
from dateutil.parser import parse as parse_datetime

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

# Toma el archivo
path = '/Users/pedrohserrano/google-takeout/Mail/Destacados.mbox'
mbox = mailbox.mbox(path)

#Extrae todas las fechas y las horas
all_times, all_dates = get_dates(mbox)
date_counts = pd.Series(all_dates).value_counts().sort_index()

date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
index = date_range.map(lambda x: str(x.date()))
date_counts = date_counts.reindex(index, fill_value=0)

date_counts.to_csv('date_counts_mails.csv', encoding='utf-8')

# Ahora se observ por mes
all_months = [x[:-3] for x in all_dates]
month_counts = pd.Series(all_months).value_counts().sort_index()

date_range = pd.date_range(start='2011-01-01', end='2017-01-01', freq='D')
months_range = date_range.map(lambda x: str(x.date())[:-3])
index = np.unique(months_range)
month_counts = month_counts.reindex(index, fill_value=0)
month_counts = pd.Series(all_months).value_counts().sort_index()

month_counts.to_csv('month_counts_mails.csv', encoding='utf-8')