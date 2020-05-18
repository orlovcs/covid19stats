import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
from dataloader import csvloader
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates



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

products_list = df.values.tolist()
print(products_list)

#plt.show() 
#df.plot('month', 'counts', kind='line', ax=ax)
#fig, ax = plt.subplots(figsize=(15,7))

#tips_passenger_df = run_query(query)
#tips_passenger_df.plot.bar(x='tip_amount', y='passenger_count', title='Passenger Amount vs. Tip Amount')
#plt.show()