
# coding: utf-8

import numpy as np
import pandas as pd
import json
import datetime
import time

import click
import boto
from boto.s3.key import Key

from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.preprocessing import StandardScaler



@click.command()
@click.option('--bucket', type=click.Path())
@click.option('--inputfile', type=click.Path())
@click.option('--outputfile', type=click.Path())
@click.option('--inicio_s', type=click.STRING)
@click.option('--final_s', type=click.STRING)
@click.option('--min_samples_c1', type=click.FLOAT)
@click.option('--min_samples_c2', type=click.FLOAT)
def main(bucket,inputfile,outputfile,inicio_s,final_s,min_samples_c1,min_samples_c2):

    conn = boto.connect_s3()
    b = conn.get_bucket(bucket)
    k = Key(b)
    k.key = inputfile
    contenido = k.get_contents_as_string()
    decodificada = contenido.decode("utf-8") 

    raw = json.loads(decodificada)
    ld = pd.DataFrame(raw['locations'])

    # In[3]:

    coords=ld[['latitudeE7','longitudeE7','timestampMs']]
    coords['timestampMs'] = coords['timestampMs'].apply(pd.to_numeric)

    # In[6]:

    #inicio_s="01/08/2016"
    #final_s="30/03/2017"
    inicio=1000*time.mktime(datetime.datetime.strptime(inicio_s, "%d/%m/%Y").timetuple())
    final=1000*time.mktime(datetime.datetime.strptime(final_s, "%d/%m/%Y").timetuple())


    # In[7]:

    coords3=coords[(coords['timestampMs']>inicio)&(coords['timestampMs']<final)]

    # In[8]:

    coords3.columns = ['lat', 'lon','timestamp']
    coords3['lat']=coords3['lat']/1e7
    coords3['lon']=coords3['lon']/1e7

    # In[9]:

    cosa=coords3[['lat','lon']]
    min_samples=np.max([len(cosa)*min_samples_c1,700])
    scaler = StandardScaler()
    scaler.fit(cosa)
    X=scaler.fit_transform(cosa)
    direcciones={}
    kms_per_radian = 6371.0088
    epsilon = 1/kms_per_radian
    db = DBSCAN(eps=epsilon, min_samples=min_samples,algorithm='ball_tree', metric='haversine').fit(X)

    # In[10]:

    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    #direcciones={}
    df_out = pd.DataFrame(columns=['lat','lon','type'])

    # In[11]:
    if (n_clusters_>0):
        clusters = [X[labels == i] for i in range(n_clusters_)]
        c0=scaler.inverse_transform(clusters[0])
        c0r=pd.DataFrame(data=c0[0:,0:])
        c0r.columns = ['lat', 'lon']
        c0r['cluster']=0

        for i in range(n_clusters_):    
            c0=scaler.inverse_transform(clusters[i])
            c0r=pd.DataFrame(data=c0[0:,0:])
            c0r.columns = ['lat', 'lon']
            lon= np.mean(c0r['lon'])
            lat= np.mean(c0r['lat'])
            df_out.loc[i]=[lat,lon,0]

    # In[12]:

    df2=X[labels == -1]
    X=df2
    min_samples=len(df2)*min_samples_c2
    db = DBSCAN(eps=epsilon, min_samples=min_samples,algorithm='ball_tree', metric='haversine').fit(X)
    labels = db.labels_
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    k.key = outputfile
    if (n_clusters_>0):
        n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
        clusters = [X[labels == i] for i in range(n_clusters_)]
        c0=scaler.inverse_transform(clusters[0])
        c0r=pd.DataFrame(data=c0[0:,0:])
        c0r.columns = ['lat', 'lon']
        c0r['cluster']=0
        direcciones={}
        for i in range(n_clusters_):    
            c0=scaler.inverse_transform(clusters[i])
            c0r=pd.DataFrame(data=c0[0:,0:])
            c0r.columns = ['lat', 'lon']
            c0r['cluster']=i
            lon= np.mean(c0r['lon'])
            lat= np.mean(c0r['lat'])
            df_out.loc[len(df_out)] = [lat,lon, 1] 
        output = df_out.to_csv(encoding='utf-8')
        k.set_contents_from_string(output)
        k.make_public()
    else: 
        #print('acabamos') 
        k.set_contents_from_string('0 clusters')
        k.make_public()       
    

if __name__ == '__main__':
    main()
