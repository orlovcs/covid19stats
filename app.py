"""Routes main function."""
import os
import subprocess
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from models import Data

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

engine = create_engine(os.environ['DATABASE_URL'])
Base = declarative_base()
Base.metadata.reflect(engine)

dt = Data()

def run_query(query):
    """Return pandas SQL query."""
    return pd.read_sql(query, con=engine)

@app.route("/")
def hello():
    """Routes main page."""
    us_infections_monthly = dt.get_monthly_totals(dt.get_us_total_infections())
    us_infections_monthly = dt.add_month_name_column(us_infections_monthly)
    months = us_infections_monthly['month_name'].tolist()
    cases = us_infections_monthly['cases'].tolist()

    us_infections_daily = dt.get_daily_totals(dt.get_us_total_infections())
    us_infections_daily = dt.add_day_name_column(us_infections_daily)
    day = us_infections_daily['day_name'].tolist()
    dcases = us_infections_daily['cases'].tolist()

    data = {}
    data['monthly'] = [months, cases]
    data['daily'] = [day, dcases]
    return render_template('dashboard/dashboard.html', data=data)
@app.route("/states.html")
def get_states():
    """Routes states page."""
    states_infections_monthly = dt.get_monthly_totals_by_state()
    all_province_states = states_infections_monthly[0]

    monthly_province_state_dfs = states_infections_monthly[1]
    dats = []
    #do this in models.py
    for dat, state in zip(monthly_province_state_dfs, all_province_states):
        months = dat[['month_name']]
        counts = dat[['cases']]
        months = months.values.tolist()
        counts = counts.values.tolist()
        #Get the scrapped data for this state
        info = dt.get_scraped_state(state)
        dat = [months, counts, info]
        dats.append(dat)

    states_infections_daily = dt.get_daily_totals_by_state()
    all_province_states = states_infections_daily[0]
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

    data = {}
    data['all_province_states'] = all_province_states
    data['all_province_states_len'] = len(all_province_states)
    data['monthly_province_state_dfs'] = dats
    data['daily_province_state_dfs'] = datss

    return render_template('dashboard/states.html', data=data)

@app.route("/about.html")
def get_about():
    """Routes about page."""
    return render_template('dashboard/about.html')

@app.route("/dash")
def get_dash():
    """Loads scrapped data with AJAX."""
    scrapped_usa_total = dt.get_scraped_usa_total()
    return render_template('dashboard/dashajax.html', scrapped_usa_total=scrapped_usa_total)

@app.route('/', methods=['PUT'])
def update_data():
    """Routes API call."""
    try:
        print("Executing data.py...")
        #Spawn subprocess for updating since request will timeout otherwise
        subprocess.Popen(["python", "data.py"])
        #Attempt to indicate progress
        #yield "x"
        return "Updated"
    except subprocess.SubprocessError as e_err:
        return str(e_err)
if __name__ == '__main__':
    app.run()
