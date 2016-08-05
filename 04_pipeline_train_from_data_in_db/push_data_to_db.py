from dbcredentials import DBCredentials 
import argparse
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
#from keras.datasets import mnist

parser = argparse.ArgumentParser(description='File with database credentials')
parser.add_argument('f', type=str,help='Full path to credential file')

NB_CLASSES = 10

if __name__ == "__main__":
    args = parser.parse_args()
    credential_file = args.f
    credentials = DBCredentials(credential_file)
    engine = create_engine(credentials.sqlalchemy_connection_string)
    connection = engine.connect()
    #remove hard coding and take schema and table as arguments
    connection.execute("DROP TABLE IF EXISTS dev.test;")
    #first write fake data to database
    data = np.arange(100).reshape(10,10)
    df = pd.DataFrame(data)
    df.to_sql(name='test',schema='dev',con=engine)
    connection.close()