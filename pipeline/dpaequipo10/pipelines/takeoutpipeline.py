__author__ = 'eduardomartinez'
# coding: utf-8
# to run, export PYTHONPATH = 'esta carpeta'
# luigi --module inicio_luigi IrisPipeline --local-scheduler

import numpy as np
import json
import os
import subprocess

import luigi
from luigi.s3 import S3Target, S3Client

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

## Logging
#import magicloop.config_ini

import logging
#logger = logging.getLogger("dpa-template.magicloop")
#logger = logging.getLogger()
logging.basicConfig(filename='takeoutpipeline.log',level=logging.ERROR)
logger = logging.getLogger()

import dpaequipo10.pipelines.utils
import dpaequipo10.pipelines.common

class TakeoutPipeline(luigi.WrapperTask):
    def requires(self):
        return {'rec':RecomendacionTask(),
                'd1':FreqBusquedasTask(),
                'd2':FreqMailTask()}


class RecomendacionTask(luigi.Task):
    bucket=luigi.Parameter()
    outputfile=luigi.Parameter()
    places=luigi.Parameter()
    radius=luigi.Parameter()

    def requires(self):
        return {'dec':BusquedasLDATask(),
                'mail':MailLDATask(),
                'ubi':UbicacionesTask()}

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net

        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-ubicacioneshtml --bucket {} --inputfile1 {} --inputfile2 {} --outputfile {} --places {} --radius {}
              '''.format(bucket_name,
                   '/modelo/dbscan_ubicaciones.csv',
                   '/categorias/categorias.csv',
                   self.outputfile,
                   self.places,
                   int(self.radius))

        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

        f = S3Target(self.bucket+'/indicadores/indicador_recomendaciones_fin.csv').open('w')
        f.write("indicador\n1\n")
        f.close()

    def output(self):
        return S3Target(self.bucket+self.outputfile)

class UbicacionesTask(luigi.Task):
    bucket=luigi.Parameter()
    inicio_s=luigi.Parameter()
    final_s=luigi.Parameter()
    min_samples_C1=luigi.Parameter()
    min_samples_C2=luigi.Parameter()
    outfile=luigi.Parameter()

    def requires(self):
        return RawDataUbicaciones()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net

        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-ubicaciones --bucket {} --inputfile {} --outputfile {} --inicio_s {} --final_s {} --min_samples_c1 {} --min_samples_c2 {}
              '''.format(bucket_name,
                   '/todas_ubicaciones.json',
                   self.outfile,
                   self.inicio_s,
                   self.final_s,
                   float(self.min_samples_C1),
                   float(self.min_samples_C2))

        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

    def output(self):
        return S3Target(self.bucket+self.outfile)

class MailLDATask(luigi.Task):
    bucket=luigi.Parameter()
    n_features=luigi.Parameter()
    n_topics=luigi.Parameter()
    n_top_words=luigi.Parameter()
    max_iter=luigi.Parameter()
    learning_method=luigi.Parameter()
    learning_offset=luigi.Parameter()
    random_state=luigi.Parameter()
    outfile=luigi.Parameter()

    def requires(self):
        return PreprocMailTask()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net
        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-lda --bucket {} --inputfile {} --n_features {} --n_topics {} --n_top_words {} --max_iter {} --learning_method {} --learning_offset {} --random_state {} --outputfile {} 
              '''.format(bucket_name,
                   '/tmp/mail.txt',
                   int(self.n_features),
                   int(self.n_topics),
                   int(self.n_top_words),
                   int(self.max_iter),
                   self.learning_method,
                   float(self.learning_offset),
                   int(self.random_state),
                   self.outfile)

        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

        f = S3Target(self.bucket+'/indicadores/indicador_analisismails_fin.csv').open('w')
        f.write("indicador\n1\n")
        f.close()

    def output(self):
        return S3Target(self.bucket+self.outfile)


class PreprocMailTask(luigi.Task):
    bucket=luigi.Parameter()
    outfile=luigi.Parameter()

    def requires(self):
        return RawDataMail()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net
        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-mail --bucket {} --inputfile {} --outputfile {} 
              '''.format(bucket_name,
                   '/todos_mails.mbox',
                   self.outfile)
        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)


        f = S3Target(self.bucket+'/indicadores/indicador_preprocmails_fin.csv').open('w')
        f.write("indicador\n1\n")
        f.close()

    def output(self):
        return S3Target(self.bucket+self.outfile)

class BusquedasLDATask(luigi.Task):
    bucket=luigi.Parameter()
    n_features=luigi.Parameter()
    n_topics=luigi.Parameter()
    n_top_words=luigi.Parameter()
    max_iter=luigi.Parameter()
    learning_method=luigi.Parameter()
    learning_offset=luigi.Parameter()
    random_state=luigi.Parameter()
    outfile=luigi.Parameter()

    def requires(self):
        return PreprocBusquedasTask()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net
        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-lda --bucket {} --inputfile {} --n_features {} --n_topics {} --n_top_words {} --max_iter {} --learning_method {} --learning_offset {} --random_state {} --outputfile {} 
              '''.format(bucket_name,
                   '/tmp/busquedas.txt',
                   int(self.n_features),
                   int(self.n_topics),
                   int(self.n_top_words),
                   int(self.max_iter),
                   self.learning_method,
                   float(self.learning_offset),
                   int(self.random_state),
                   self.outfile)

        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

    def output(self):
        return S3Target(self.bucket+self.outfile)

#task
class PreprocBusquedasTask(luigi.Task):
    bucket=luigi.Parameter()
    outfile=luigi.Parameter()

    def requires(self):
        return RawDataBusquedas()

    def run(self):
        with self.input().open('r') as data_file:
          data = json.load(data_file)

        f = self.output().open('w')

        for query in data['event']:
          query_text = query['query']['query_text']
          f.write(query_text)
          f.write('\n')
        f.close()

    def output(self):
        return S3Target(self.bucket+self.outfile)

class FreqMailTask(luigi.Task):
    bucket=luigi.Parameter()
    outputfile1=luigi.Parameter()
    outputfile2=luigi.Parameter()
    fecha_i=luigi.Parameter()
    fecha_f=luigi.Parameter()

    def requires(self):
        return RawDataMail()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net

        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-freqmail --bucket {} --inputfile {} --outputfile1 {} --outputfile2 {} --fecha_i {} --fecha_f {}
              '''.format(bucket_name,
                   '/todos_mails.mbox',
                   self.outputfile1,
                   self.outputfile2,
                   self.fecha_i,
                   self.fecha_f)
        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

    def output(self):
        return {'out1':S3Target(self.bucket+self.outputfile1),
                'out2':S3Target(self.bucket+self.outputfile2)}

class FreqBusquedasTask(luigi.Task):
    bucket=luigi.Parameter()
    outputfile1=luigi.Parameter()
    outputfile2=luigi.Parameter()
    fecha_i=luigi.Parameter()
    fecha_f=luigi.Parameter()

    def requires(self):
        return RawDataBusquedas()

    def run(self):
        bucket_name=self.bucket[5:]
        #--network dpaequipo10_net

        cmd = '''
              docker run --rm -v dpaequipo10_store:/dpaequipo10/data --env-file ./.env localhost:5000/dpaequipo10/test-python-freqbusq --bucket {} --inputfile {} --outputfile1 {} --outputfile2 {} --fecha_i {} --fecha_f {}
              '''.format(bucket_name,
                   '/todas_busquedas.json',
                   self.outputfile1,
                   self.outputfile2,
                   self.fecha_i,
                   self.fecha_f)
        logger.debug(cmd)
        out = subprocess.call(cmd, shell=True)
        logger.debug(out)

    def output(self):
        return {'out1':S3Target(self.bucket+self.outputfile1),
                'out2':S3Target(self.bucket+self.outputfile2)}

#external
class RawDataBusquedas(luigi.ExternalTask):
    bucket = luigi.Parameter()
    def output(self):
        output_path = '{}/todas_busquedas.json'.format(self.bucket)
        return S3Target(output_path)

class RawDataUbicaciones(luigi.ExternalTask):
    bucket = luigi.Parameter()
    def output(self):
        output_path = '{}/todas_ubicaciones.json'.format(self.bucket)
        return S3Target(output_path)

class RawDataMail(luigi.ExternalTask):
    bucket = luigi.Parameter()
    def output(self):
        output_path = '{}/todos_mails.mbox'.format(self.bucket)
        return S3Target(output_path)
