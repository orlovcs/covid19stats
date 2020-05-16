import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
from dataloader import csvloader
import matplotlib.pyplot as plt

#export PG_HOME=/Library/PostgreSQL/12 
#export PATH=$PATH:$PG_HOME/bin

database = 'nyc_taxi'

#connect to the database
connection = pg.connect("dbname=nyc_taxi user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

engine = create_engine('postgresql://postgres:root@localhost/nyc_taxi')

#initiate loading csv
csvloader(engine, '../datasets/green_tripdata_2019-01.csv', 'green_tripdata_2019')

#query demos

def run_command(command):
   cursor.execute(command)
   print(cursor.statusmessage)

def print_query(query):
   print(pd.read_sql(query, con=engine))

def run_query(query):
   return pd.read_sql(query, con=engine)

#Let's plot the passenger amount vs. tip amount

query = 'SELECT lpep_pickup_datetime, total_amount, passenger_count, tip_amount FROM green_tripdata_2019 WHERE tip_amount > 0 LIMIT 2000;'
print_query(query)

tips_passenger_df = run_query(query)
tips_passenger_df.plot.bar(x='tip_amount', y='passenger_count', title='Passenger Amount vs. Tip Amount')
plt.show()