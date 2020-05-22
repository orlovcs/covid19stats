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
import time


#export PG_HOME=/Library/PostgreSQL/12
#export PATH=$PATH:$PG_HOME/bin

#connect to the database
connection = pg.connect("dbname=covid user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

engine = create_engine('postgresql://postgres:root@localhost/covid')

#initiate loading csv
csvloader(engine, '../datasets/us_confirmed.csv', 'us_infections')

def run_command(command):
   cursor.execute(command)
   print(cursor.statusmessage)

def print_query(query):
   print(pd.read_sql(query, con=engine))

def run_query(query):
   return pd.read_sql(query, con=engine)

query = 'SELECT * FROM us_infections;'
df = run_query(query)

df['day'] = pd.to_datetime(df['date']).dt.to_period('D')

#END OF MONTH CASES IN US
monthyl_us_df = df.groupby(['day','date'])['cases'].sum().reset_index()
monthyl_us_df = monthyl_us_df.iloc[df.reset_index().groupby(pd.to_datetime(monthyl_us_df['date']).dt.to_period('M'))['index'].idxmax()]

#END OF MONTH CASES IN AL
monthly_al_df = df.loc[df['province_state'] == 'Alabama']
monthly_al_df = monthly_al_df.groupby(['day','date'])['cases'].sum().reset_index()
monthly_al_df = monthly_al_df.iloc[df.reset_index().groupby(pd.to_datetime(monthly_al_df['date']).dt.to_period('M'))['index'].idxmax()]

#LIST OF UNIQUE province_state VALUES
all_province_state = df.province_state.unique()
print(all_province_state)

#GET MONTHLY CASES FOR EVERY province_state
monthly_province_state_dfs = []
for province_state in all_province_state:
    new_monthly_df = df.loc[df['province_state'] == province_state]
    new_monthly_df = new_monthly_df.groupby(['day','date'])['cases'].sum().reset_index()
    new_monthly_df = new_monthly_df.iloc[df.reset_index().groupby(pd.to_datetime(new_monthly_df['date']).dt.to_period('M'))['index'].idxmax()]
    monthly_province_state_dfs.append(new_monthly_df)
print(len(monthly_province_state_dfs))

#df.sort_values('day').groupby('day').tail(1)
#print(df.tail())

#df11 = df.groupby(['date'])['cases'].sum().reset_index()
#df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
#df = df.sort_values('date').groupby('month').tail(1)
#print(df.head())

# df = df.groupby(['month']).size().reset_index(name='counts')
# df['month'] = df['month'].apply(lambda x: x.strftime('%b'))


# month_list = df.values.tolist()

# month = [l[0] for l in month_list]


# query = 'SELECT index, date FROM us_infections;'
# df = run_query(query)
# #convert the dates to a day Period column
# df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
# df = df.groupby(['day']).size().reset_index(name='counts')
# df['sum'] = df['counts'].cumsum()
# print(df.tail(n=15))

# query = 'SELECT count(*) FROM us_infections WHERE date=\'2020-01-22\';'
# print_query(query)
