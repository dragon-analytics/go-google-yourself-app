import sys
import os

import numpy as np
import pandas as pd
import click
import boto
from boto.s3.key import Key

from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation




#esto debe regresar un array de tokens
def print_top_words(model, feature_names, n_top_words):
    array = []
    for topic_idx, topic in enumerate(model.components_):
        #print("Topic #%d:" % topic_idx)
        array.append(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    return '\n'.join(array)


@click.command()
@click.option('--bucket', type=click.Path())
@click.option('--inputfile', type=click.Path())
@click.option('--n_features', type=click.INT)
@click.option('--n_topics', type=click.INT)
@click.option('--n_top_words', type=click.INT)
@click.option('--max_iter', type=click.INT)
@click.option('--learning_method', type=click.STRING)
@click.option('--learning_offset', type=click.FLOAT)
@click.option('--random_state', type=click.INT)
@click.option('--outputfile', type=click.Path())
def main(bucket,inputfile,n_features,n_topics,n_top_words,max_iter,learning_method,learning_offset,random_state,outputfile):
    print("inicia main LDA")

    conn = boto.connect_s3()
    b = conn.get_bucket(bucket)
    k = Key(b)
    k.key = inputfile
    contenido = k.get_contents_as_string()
    
    decodificada = contenido.decode("utf-8") 
    
    data_samples = np.array(decodificada.split('\n'))

    n_samples = len(data_samples)

    print("leyo de S3 y existen {} samples".format(n_samples))

    # Use tf-idf features for NMF.
    print("Extracting tf-idf features for NMF...")
    tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=n_features,
                                       stop_words='english')
    #t0 = time()
    tfidf = tfidf_vectorizer.fit_transform(data_samples)
    #print("done in %0.3fs." % (time() - t0))

    # Use tf (raw term count) features for LDA.
    print("Extracting tf features for LDA...")
    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                    max_features=n_features,
                                    stop_words='english')
    #t0 = time()
    tf = tf_vectorizer.fit_transform(data_samples)
    #print("done in %0.3fs." % (time() - t0))

    # PRUEBAS CON NMF
    # Fit the NMF model
    # print("Fitting the NMF model with tf-idf features, "
    #       "n_samples=%d and n_features=%d..."
    #       % (n_samples, n_features))
    # #t0 = time()
    # nmf = NMF(n_components=n_topics, random_state=1,
    #           alpha=.1, l1_ratio=.5).fit(tfidf)
    # #print("done in %0.3fs." % (time() - t0))

    # print("\nTopics in NMF model:")
    # tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    # print_top_words(nmf, tfidf_feature_names, n_top_words)

    

    print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..."
          % (n_samples, n_features))
    lda = LatentDirichletAllocation(n_topics=n_topics, max_iter=max_iter,
                                    learning_method=learning_method,
                                    learning_offset=learning_offset,
                                    random_state=random_state)
    #t0 = time()
    lda.fit(tf)
    #print("done in %0.3fs." % (time() - t0))

    print("\nTopics in LDA model:")
    tf_feature_names = tf_vectorizer.get_feature_names()


    cadena = print_top_words(lda, tf_feature_names, n_top_words)
    # buscar un set contents distinto para escribir: array
    k.key = outputfile
    k.set_contents_from_string(cadena)
    k.make_public()

if __name__ == '__main__':
    main()
