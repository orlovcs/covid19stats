import psycopg2 as pg
import pandas as pd
import io
import os
from sqlalchemy import create_engine
import numpy as np
import datetime
import time
import requests
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, WebDriverException
from selenium.webdriver.chrome.options import Options as ChromeOptions
import sys

print("Starting update.")

engine = create_engine(os.environ['DATABASE_URL'])

def run_query(query):
   return pd.read_sql(query, con=engine)

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

print("CSV Tables Updated")



#Check if Selenium Chromedriver should be initialized with the docker method
docker_config = False
args_amt = len(sys.argv)
if args_amt == 2:
   if sys.argv[1] == 'docker' or sys.argv[1] == '-docker':
      print("Docker Chromedriver method selected")
      docker_config = True




print("Initializing Selenium Driver")

driver = None
scraped_usa_total = []
scraped_states_dict = {}
#init the chrome driver
#Able to work on the heroku dyno and local system server
options = ChromeOptions()

#Check if Docker method selected for this env var
if docker_config == False:
   chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
   options.binary_location = chrome_bin
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

#Let the driver attempt to start for only a certain amount of times if it is unstable before giving up
maxcounter=5
for counter in range(maxcounter):
   try:
      if docker_config:        
         driver = webdriver.Chrome(chrome_options=options)
      else:
         driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)
      break
   except WebDriverException as e:
      print("RETRYING THE INITIALIZATION OF WEBDRIVER! Error: %s" % str(e))
      time.sleep(10)
      if counter==maxcounter-1:
         driver = None

if driver:
   #Scrap info cards will only be displayed if elements are found
   try:
      driver.get("https://www.worldometers.info/coronavirus/country/us/")
      tbody = driver.find_element_by_tag_name("tbody")
      #Grab just the first total row
      for row in tbody.find_elements_by_tag_name("tr"):
            cells = row.find_elements_by_tag_name("td")
            for cell in cells:
               scraped_usa_total.append(cell.text)
            break
      #Grab every row for all states
      for row in tbody.find_elements_by_tag_name("tr"):
            cells = row.find_elements_by_tag_name("td")
            state_row = []
            for cell in cells:
               state_row.append(cell.text)
               scraped_states_dict[state_row[0]] = state_row
      #Grab provinces
      tbody = driver.find_element_by_xpath("//*[@id='usa_table_countries_today']/tbody[2]")
      for row in tbody.find_elements_by_tag_name("tr"):
            cells = row.find_elements_by_tag_name("td")
            state_row = []
            for cell in cells:
               state_row.append(cell.text)
               scraped_states_dict[state_row[0]] = state_row
      driver.close()

   except NoSuchElementException:
      scraped_usa_total = None


if scraped_usa_total:
   #Change white spaces to 0
   scraped_usa_total = [x.replace('', '0') if x == '' else x for x in scraped_usa_total]
   scraped_usa_total = [x.replace(' ', '0') if x == '' else x for x in scraped_usa_total]

   #Make a table for us total scrap dash with this list
   df = pd.DataFrame(scraped_usa_total,columns=['values'])
   table = 'us total scrap'
   try:
      df.to_sql(table, engine, if_exists='replace')
   except ValueError:
         print('Table '+table+' already exists, doing nothing')

   print("Table us total scrap updated")

#make sure all scraped tables are available
if scraped_states_dict and len(scraped_states_dict) > 52:
   #Reformat table names from scrapped data
   #No info on American Samoa
   scraped_states_dict['American Samoa'] = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
   #Reformat D.C
   scraped_states_dict['District of Columbia'] = scraped_states_dict['District Of Columbia']
   del(scraped_states_dict['District Of Columbia'])
   #Reformat A.V.I.
   scraped_states_dict['Virgin Islands'] = scraped_states_dict['United States Virgin Islands']
   del(scraped_states_dict['United States Virgin Islands'])
   #Cruise Ships need to be formatted
   scraped_states_dict['Diamond Princess'] = scraped_states_dict['Diamond Princess Ship']
   del(scraped_states_dict['Diamond Princess Ship'])

   scraped_states_dict['Grand Princess'] = scraped_states_dict['Grand Princess Ship']
   del(scraped_states_dict['Grand Princess Ship'])

   

   #Will there be a state ending with scrap?
   #Add a signifier to the end of every state
   scraped_states_dict =  {k+" scrap": v for k, v in scraped_states_dict.items()}

   #Create a table for every state scrapped data
   for province_state in province_states:
      #Trim off un-needed stats, keep indicies 1,3,6,7
      state_scrap_info = scraped_states_dict[province_state + " scrap"]
      scraped_states_dict[province_state + " scrap"] = [state_scrap_info[1],state_scrap_info[3],state_scrap_info[6],state_scrap_info[7]]

      #Replace all white space with N/A
      scraped_states_dict[province_state + " scrap"] = [x.replace('', 'N/A') if x == '' else x for x in scraped_states_dict[province_state + " scrap"]]
      
      df = pd.DataFrame(scraped_states_dict[province_state + " scrap"],columns=['values'])
      table = province_state + " scrap"
      try:
         df.to_sql(table, engine, if_exists='replace')
      except ValueError:
            print('Table '+table+' already exists, doing nothing') 
   print("State scrap tables updated")