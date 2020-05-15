import psycopg2 as pg
import pandas as pd
import io
from sqlalchemy import create_engine
from dataloader import loader

#export PG_HOME=/Library/PostgreSQL/12 
#export PATH=$PATH:$PG_HOME/bin

#connect to the database
connection = pg.connect("dbname=consumer_complaints user=postgres password=root")
#open a cursor for interaction
cursor = connection.cursor()

#engine = create_engine('postgresql://postgres@localhost/consumer_complaints')

#refresh tables
#cursor.execute("DROP TABLE bank_account_complaints;")
#cursor.execute("DROP TABLE credit_card_complaints;")
#cursor.execute("DROP TABLE credit_card_complaints_df;")

#create the bank_account_complaints table
cursor.execute("CREATE TABLE IF NOT EXISTS bank_account_complaints (\
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
cursor.execute("CREATE TABLE IF NOT EXISTS  credit_card_complaints (\
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

#initiate loading csv
loader()



#make execution changes permanant
connection.commit()

#tst = cursor.fetchone()
#print(tst)
