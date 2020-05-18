import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
from dataloader import csvloader
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import datetime



#export PG_HOME=/Library/PostgreSQL/12 
#export PATH=$PATH:$PG_HOME/bin

#connect to the database
connection = pg.connect("dbname=covid user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

engine = create_engine('postgresql://postgres:root@localhost/covid')

#initiate loading csv
csvloader(engine, '../datasets/us_confirmed.csv', 'us_infections')

#query demos

def run_command(command):
   cursor.execute(command)
   print(cursor.statusmessage)

def print_query(query):
   print(pd.read_sql(query, con=engine))

def run_query(query):
   return pd.read_sql(query, con=engine)

#Let's plot the passenger amount vs. tip amount

#query = 'SELECT * FROM us_confirmed WHERE "province/state"=\'Arizona\';'
query = 'SELECT index, date FROM us_infections;'
df = run_query(query) 

df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
df = df.groupby(['month']).size().reset_index(name='counts')
df['month'] = df['month'].apply(lambda x: x.strftime('%b'))


month_list = df.values.tolist()

month = [l[0] for l in month_list]


query = 'SELECT index, date FROM us_infections;'
df = run_query(query)
#convert the dates to a day Period column
df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
df = df.groupby(['day']).size().reset_index(name='counts')
df['sum'] = df['counts'].cumsum()
print(df.tail(n=15))

query = 'SELECT count(*) FROM us_infections WHERE date=\'2020-01-22\';'
print_query(query)
