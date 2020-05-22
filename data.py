import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
import numpy as np
import datetime
import time
from sqlalchemy.types import TEXT


#connect to the database
connection = pg.connect("dbname=covid user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

engine = create_engine('postgresql://postgres:root@localhost/covid')



def run_command(command):
   cursor.execute(command)
   print(cursor.statusmessage)

def print_query(query):
   print(pd.read_sql(query, con=engine))

def run_query(query):
   return pd.read_sql(query, con=engine)



def csvloader(engine, file, table):
  
   #copy data from csv file
   my_file = open(file)
   df = pd.read_csv(my_file)
   #lowercase column names
   df.columns = map(str.lower, df.columns)
   #remove all whitespaces, replace them with underscores
   df = df.rename(columns=lambda x: x.replace(' ', '_'))
   df = df.rename(columns=lambda x: x.strip())
   
   df = df.rename(columns={'country/region': 'country_region', 'province/state': 'province_state', 'case':'cases'})

   df = df[['combined_key', 'date', 'country_region', 'cases', 'province_state']]

   print(df.head(n=10))

   #if table does not exist, add it to the dbs
     #if table does not exist, add it to the dbs
   try:
      df.to_sql(table, engine, if_exists='fail')
   except ValueError:
        print('Table '+table+' already exists, doing nothing')
      
   #after main table is added, create the additional aggregated table




#initiate loading csv
csvloader(engine, '../datasets/us_confirmed.csv', 'us_infections')

query = 'SELECT * FROM us_infections;'
df = run_query(query)
province_states = df.province_state.drop_duplicates()

#Create a table for all states
table = 'states'
try:
   province_states.to_sql(table, engine, if_exists='fail')
except ValueError:
      print('Table '+table+' already exists, doing nothing')

#Create total cases in America table
query = 'SELECT date, SUM(cases) AS cases FROM us_infections GROUP BY date;'
df = run_query(query)
table = 'us total'
try:
   df.to_sql(table, engine, if_exists='fail')
except ValueError:
      print('Table '+table+' already exists, doing nothing')

#Create total cases table for every state
for province_state in province_states:
   query = 'SELECT date, SUM(cases) AS cases FROM us_infections WHERE province_state=\''+province_state+'\' GROUP BY date;'
   df = run_query(query)
   table = province_state
   try:
      df.to_sql(table, engine, if_exists='fail')
   except ValueError:
         print('Table '+table+' already exists, doing nothing') 