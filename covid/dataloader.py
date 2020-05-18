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
   
   df = df.rename(columns={'country/region': 'country_region', 'province/state': 'province_state'})

   print(df.head(n=10))

   #if table does not exist, add it to the dbs
     #if table does not exist, add it to the dbs
   try:
      df.to_sql(table, engine, if_exists='replace')
   except ValueError:
        print('Table '+table+' already exists, doing nothing')