from dbcredentials import DBCredentials 
import argparse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
#from keras.datasets import mnist

#{{database}}, {{host}}, {{port}}, {{user}}, {{password}}
parser = argparse.ArgumentParser(description='File with database credentials')
parser.add_argument('d', type=str,help='database')
parser.add_argument('h', type=str,help='host')
parser.add_argument('p', type=str,help='port')
parser.add_argument('u', type=str,help='user')
parser.add_argument('pw', type=str,help='password')


NB_CLASSES = 10

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
    #remove hard coding and take schema and table as arguments
    connection.execute("DROP TABLE IF EXISTS dev.test;")
    #first write fake data to database
    data = np.arange(100).reshape(10,10)
    df = pd.DataFrame(data)
    df.to_sql(name='test',schema='dev',con=engine)
    connection.close()