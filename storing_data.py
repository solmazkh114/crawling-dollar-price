import psycopg2
import pandas as pd
from sqlalchemy import create_engine




class store_on_database:
    def __init__(self, database='rec_task', user="postgres", filepath="data/history_dollar_price.csv", table='dollar_price'):
        self.database = database
        self.user = user
        self.filepath = filepath
        self.table = table
    def __create_connection(self):
        self.password = input("Please enter your PostgreSQL password")
        connection = psycopg2.connect(user= self.user, password= self.password, database= self.database)
        cursor = connection.cursor()
        return connection, cursor
    def store_data(self):
        connection, cursor = self.__create_connection()
        df = pd.read_csv(self.filepath)
        engine = create_engine('postgresql://postgres:'+self.password+'@localhost:5432/'+self.database)
        df.to_sql(self.table, engine)

