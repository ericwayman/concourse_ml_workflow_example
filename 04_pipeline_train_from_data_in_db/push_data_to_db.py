from dbcredentials import DBCredentials 
import argparse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
from keras.datasets import mnist
import os

def transform_data(data):
    """Reshape/transform the MNIST dataset."""
    (X_train, y_train), (X_test, y_test) = data
    X_train = X_train.reshape(60000, 784)
    X_test = X_test.reshape(10000, 784)
    X_train = X_train.astype("float32")
    X_test = X_test.astype("float32")
    X_train /= 255
    X_test /= 255

    return X_train, X_test, y_train, y_test

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
    TEST_TABLE = os.environ.get('TEST_TABLE')
    TRAIN_TABLE = os.environ.get('TRAIN_TABLE')

    #fetch data
    X_train, X_test, y_train, y_test = transform_data(mnist.load_data())
    print("loaded data")
    #add train data to database
    df_train = pd.DataFrame(X_train).iloc[:100,:]
    df_train['target'] = y_train[:100]
    print("configured df_train")
    connection.execute("DROP TABLE IF EXISTS {schema}.{train_table};".format(schema = SCHEMA, train_table = TRAIN_TABLE))
    print('dropped train table')

    df_train.to_sql(name=TRAIN_TABLE,schema=SCHEMA,con=engine)
    print('wrote train data to sql')
    
    #add test data to database
    df_test = pd.DataFrame(X_test).iloc[:100,:]
    df_test['target'] = y_test[:100]
    print('configured df_test')
    connection.execute("DROP TABLE IF EXISTS {schema}.{test_table};".format(schema = SCHEMA, test_table = TEST_TABLE))
    print('dropped test table')
    df_test.to_sql(name=TEST_TABLE,schema=SCHEMA,con=engine)
    print('wrote test data to sql')
    connection.close()
    print('done')