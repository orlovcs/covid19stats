import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
import time, datetime



app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
engine = create_engine(os.environ['DATABASE_URL'])

Base = declarative_base()

Base.metadata.reflect(engine)

from models import Data, Infections




dt = Data()



def run_query(query):
   return pd.read_sql(query, con=engine)

@app.route("/")
def hello():

    scrapped_usa_total = dt.get_scraped_usa_total()


    us_infections_monthly = dt.get_monthly_totals(dt.get_us_total_infections())
    us_infections_monthly = dt.add_month_name_column(us_infections_monthly)
    us_infections_monthly_html = dt.df_to_html(us_infections_monthly)
    months = us_infections_monthly['month_name'].tolist()
    cases = us_infections_monthly['cases'].tolist()


    us_infections_daily = dt.get_daily_totals(dt.get_us_total_infections())
    us_infections_daily = dt.add_day_name_column(us_infections_daily)
    day = us_infections_daily['day_name'].tolist()
    dcases = us_infections_daily['cases'].tolist()

    
    return render_template('dashboard/dashboard.html', scrapped_usa_total=scrapped_usa_total, us_infections_monthly_list=[months,cases], us_infections_daily_list=[day, dcases]  )
@app.route("/states.html")
def get_states():
    try:

        scraped_states_dict = dt.get_scraped_states_dict()

        states_infections_monthly = dt.get_monthly_totals_by_state()
        all_province_states = states_infections_monthly[0]
        all_province_states_stripped = [x.strip(' ') for x in all_province_states]

        monthly_province_state_dfs = states_infections_monthly[1]
        dats = []
        #do this in models.py
        for dat, state in zip(monthly_province_state_dfs, all_province_states):
            months = dat[['month_name']]
            counts = dat[['cases']]
            months = months.values.tolist() 
            counts = counts.values.tolist() 
            info = []
            #make sure all scraped tables are available
            if len(scraped_states_dict) > 52:
                #No info on American Samoa
                if state == 'American Samoa':
                    info = ['N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A', 'N/A']
                #Reformat D.C
                elif state == 'District of Columbia':
                    info = scraped_states_dict['District Of Columbia']
                #Reformat A.V.I.
                elif state == 'Virgin Islands':
                    info = scraped_states_dict['United States Virgin Islands']
                #Cruise Ships need to be formatted
                elif state == 'Diamond Princess':
                    info = scraped_states_dict['Diamond Princess Ship']
                elif state == 'Grand Princess':
                    info = scraped_states_dict['Grand Princess Ship']            
                elif state in scraped_states_dict:
                    info = scraped_states_dict[state]
            dat = [months, counts, info]
            dats.append(dat)


        states_infections_daily = dt.get_daily_totals_by_state()
        all_province_states = states_infections_daily[0]
        all_province_states_stripped = [x.strip(' ') for x in all_province_states]

        daily_province_state_dfs = states_infections_daily[1]
        datss = []
        #do this in models.py
        for dat in daily_province_state_dfs:
            days = dat[['day_name']]
            counts = dat[['cases']]
            days = days.values.tolist() 
            counts = counts.values.tolist() 
            dat = [days, counts]
            datss.append(dat)


        

        return render_template('dashboard/states.html', all_province_states=all_province_states, all_province_states_stripped=all_province_states_stripped, all_province_states_len=len(all_province_states),  monthly_province_state_dfs=dats,  daily_province_state_dfs=datss )
    except Exception as e:
	    return(str(e))


@app.route("/about.html")
def get_about():
    try:
        return render_template('dashboard/about.html')
    except Exception as e:
	    return(str(e))


if __name__ == '__main__':
    app.run()
