import psycopg2 as pg
import pandas as pd
import io
import os
from sqlalchemy import create_engine
import numpy as np
import datetime
import time
import requests


engine = create_engine(os.environ['DATABASE_URL'])

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
      

#downloaded updated dataset
response = requests.get('http://datahub.io/core/covid-19/r/us_confirmed.csv')
file_object = io.StringIO(response.content.decode('utf-8'))
us_confirmed_df = pd.read_csv(file_object)

us_confirmed_df.columns = map(str.lower, us_confirmed_df.columns)
#remove all whitespaces, replace them with underscores
us_confirmed_df = us_confirmed_df.rename(columns=lambda x: x.replace(' ', '_'))
us_confirmed_df = us_confirmed_df.rename(columns=lambda x: x.strip())
us_confirmed_df = us_confirmed_df.rename(columns={'country/region': 'country_region', 'province/state': 'province_state', 'case':'cases'})
us_confirmed_df = us_confirmed_df[['combined_key', 'date', 'country_region', 'cases', 'province_state']]


#initiate loading csv
#csvloader(engine, '../datasets/us_confirmed.csv', 'us_infections')

province_states = us_confirmed_df.province_state.drop_duplicates()

#Create a table for all states
table = 'states'
try:
   province_states.to_sql(table, engine, if_exists='replace')
except ValueError:
      print('Table '+table+' already exists, doing nothing')

#Create total cases in America table


#Pandas equivalent statement for 'SELECT date, SUM(cases) AS cases FROM us_infections GROUP BY date;'
# df = run_query(query)
df = us_confirmed_df.groupby(['date'])['cases'].sum()

table = 'us total'
try:
   df.to_sql(table, engine, if_exists='replace')
except ValueError:
      print('Table '+table+' already exists, doing nothing')

#Create total cases table for every state
for province_state in province_states:
   #Pandas equivalent statement for  'SELECT date, SUM(cases) AS cases FROM us_infections WHERE province_state=\''+province_state+'\' GROUP BY date;'
   df = us_confirmed_df[us_confirmed_df.province_state == province_state]
   df = df.groupby(['date'])['cases'].sum()
   table = province_state
   try:
      df.to_sql(table, engine, if_exists='replace')
   except ValueError:
         print('Table '+table+' already exists, doing nothing') 

print("Tables Updated")