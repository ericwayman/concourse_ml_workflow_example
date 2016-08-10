from dbcredentials import DBCredentials 
import argparse
from sqlalchemy import create_engine
import pandas as pd
import sys
import os
import datetime
import numpy as np
import yaml
np.random.seed(1337)
from keras.datasets import mnist
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from sqlalchemy import create_engine
from time import time 

NB_CLASSES = 10

def load_data(engine,schema,table,target='target'):
    '''
    load data from data base and return data frames suitable for training or testing
    '''
    query = 'SELECT * FROM {schema}.{table}'.format(schema=schema,table = table)
    df = pd.read_sql(sql=query,con=engine,index_col='index')
    y = df.as_matrix([target]).flatten()
    X = df.drop([target], axis=1).as_matrix()
    return X, y

def evaluate_model(X_train, X_test, y_train, y_test, batch_size, nb_epoch):
    """Returns loss/accuracy and the model."""
    model = Sequential()
    model.add(Dense(512, input_shape=(784,)))
    model.add(Activation("relu"))
    model.add(Dropout(0.2))
    model.add(Dense(512))
    model.add(Activation("relu"))
    model.add(Dropout(0.2))
    model.add(Dense(10))
    model.add(Activation("softmax"))
    model.compile(loss="categorical_crossentropy",
              optimizer=RMSprop(),
              metrics=["accuracy"])
    model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=nb_epoch,
            verbose=1, validation_data=(X_test, y_test))
    results = model.evaluate(X_test, y_test, verbose=0)
    return results, model

parser = argparse.ArgumentParser(description='File with database credentials')
parser.add_argument('d', type=str,help='database')
parser.add_argument('h', type=str,help='host')
parser.add_argument('p', type=str,help='port')
parser.add_argument('u', type=str,help='user')
parser.add_argument('pw', type=str,help='password')

if __name__ == "__main__":
    args = parser.parse_args()
    database = args.d
    host = args.h
    port = args.p
    user = args.u
    password = args.pw
    credentials = DBCredentials(database, host, port, user, password)
    engine = create_engine(credentials.sqlalchemy_connection_string)
    connection = engine.connect()

    #fetch schema and table names
    SCHEMA = os.environ.get('SCHEMA')
    TEST_TABLE =  os.environ.get('TEST_TABLE')
    TRAIN_TABLE = os.environ.get('TRAIN_TABLE')

    #fetch training parameters
    BATCH_SIZE = int(os.environ.get('BATCH_SIZE'))
    NB_EPOCH = int(os.environ.get('NB_EPOCH'))

    X_train, y_train = load_data(engine, schema = SCHEMA, table = TRAIN_TABLE)
    X_test, y_test = load_data(engine, schema = SCHEMA, table = TEST_TABLE)
    y_train = np_utils.to_categorical(y_train, NB_CLASSES)
    y_test = np_utils.to_categorical(y_test, NB_CLASSES)
    logfile = "new_log_dir/model.log"
    with open(logfile,'w') as f:
      sys.stdout = f
      evaluate_model(X_train, X_test, y_train, y_test, BATCH_SIZE, NB_EPOCH)



