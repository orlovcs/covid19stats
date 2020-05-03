import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine

#export PG_HOME=/Library/PostgreSQL/12 
#export PATH=$PATH:$PG_HOME/bin

#connect to the database
connection = pg.connect("dbname=consumer_complaints user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

#engine = create_engine('postgresql://postgres@localhost/consumer_complaints')

#refresh tables
cursor.execute("DROP TABLE bank_account_complaints;")
cursor.execute("DROP TABLE credit_card_complaints;")

#create the bank_account_complaints table
cursor.execute("CREATE TABLE bank_account_complaints (\
 complaint_id text PRIMARY KEY,\
 date_received date,\
 product text,\
 sub_product text,\
 issue text,\
 sub_issue text,\
 consumer_complaint_narrative text,\
 company_public_response text,\
 company text,\
 state text,\
 zip_code text,\
 tags text,\
 consumer_consent_provided text,\
 submitted_via text,\
 date_sent date,\
 company_response_to_consumer text,\
 timely_response text,\
 consumer_disputed text);;")

#create the credit_card_complaints table
cursor.execute("CREATE TABLE credit_card_complaints (\
 complaint_id text PRIMARY KEY,\
 date_received date,\
 product text,\
 sub_product text,\
 issue text,\
 sub_issue text,\
 consumer_complaint_narrative text,\
 company_public_response text,\
 company text,\
 state text,\
 zip_code text,\
 tags text,\
 consumer_consent_provided text,\
 submitted_via text,\
 date_sent date,\
 company_response_to_consumer text,\
 timely_response text,\
 consumer_disputed text);;")
print("oiw")
 #copy data from csv file
my_file = open("datasets/Credit_Card_Complaints.csv")
df = pd.read_csv(my_file)
#convert df to file-like object in order to use the efficient psycopg copy functions
#buffer = io.StringIO()
#df.to_csv(buffer, header=False, index=False)
#buffer.pos = 0
#copy in data
#cursor.copy_from(buffer, 'credit_card_complaints', sep=',')




print("oi")
for complaint in df:
   print(complaint[complaint_id])





#removes table after we are done
#cursor.execute("DROP TABLE bank_account_complaints;")
#cursor.execute("DROP TABLE credit_card_complaints;")

#make execution changes permanant
connection.commit()

#tst = cursor.fetchone()
#print(tst)
