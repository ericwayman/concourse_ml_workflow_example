"""
A class to represent the credentials to connect to a postgres database with psycopg2
Credentials are stored in a yaml file with keys:
host, port, user, database, password
"""
import yaml

class DBCredentials: 

    def __init__(self,credential_file):
        """
        params ::credential_file::string The full path of the user credential file
        """
        #Read database credentials from user supplied file
        self.credential_file = credential_file
        with open(self.credential_file,'r') as stream:
            yml = yaml.load(stream)

        #host, port, user, database, password
        self.host = yml['host']
        self.port = yml['port']
        self.user = yml['user']
        self.database = yml['database']
        self.password = yml['password']

    @property
    def psyopg2_connection_string(self):
        """
           Return the connection string associated with the user_credential_file
        """
        #Initialize connection string
        conn_str =  """dbname='{database}' user='{user}' host='{host}' port='{port}' password='{password}'""".format(                       
                        database=self.database,
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        password=self.password
                )
        return conn_str

    @property
    def sqlalchemy_connection_string(self):
        """
           Return the connection string associated with the user_credential_file
        """
        #Initialize connection string
        conn_str =  """postgresql://{user}:{password}@{host}:{port}/{database}""".format(                       
                        database=self.database,
                        host=self.host,
                        port=self.port,
                        user=self.user,
                        password=self.password
                )
        return conn_str