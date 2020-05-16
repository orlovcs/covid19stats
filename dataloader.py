from sqlalchemy.types import TEXT

import pandas as pd

def csvloader(engine, file, table):
  
   #copy data from csv file
   my_file = open(file)
   df = pd.read_csv(my_file)
   #lowercase column names
   df.columns = map(str.lower, df.columns)
   #remove all whitespaces, replace them with underscores
   df = df.rename(columns=lambda x: x.replace(' ', '_'))
   df = df.rename(columns=lambda x: x.strip())
   
   #print(df.head(n=10))

   #if table does not exist, add it to the dbs
   try:
      df.to_sql(table, engine, if_exists='fail',dtype={col_name: TEXT for col_name in df if col_name != 'index' or col_name != 'complaint_id'})
   except ValueError:
        print('Table '+table+' already exists, doing nothing')