import pandas as pd
from sqlalchemy import create_engine

def loader():
   engine = create_engine('postgresql://postgres:root@localhost/consumer_complaints')
   #dialect+driver://username:password@host:port/database
   #('postgresql://postgres@localhost/consumer_complaints')

   #copy data from csv file
   my_file = open("datasets/Credit_Card_Complaints.csv")
   df = pd.read_csv(my_file)
   #lowercase column names
   df.columns = map(str.lower, df.columns)
   #remove all whitespaces, replace them with underscores
   df = df.rename(columns=lambda x: x.replace(' ', '_'))
   df = df.rename(columns=lambda x: x.strip())
   
   print(df.head(n=10))

   df.to_sql('credit_card_complaints_df', engine, if_exists='replace')
