from app import db
import pandas as pd
from sqlalchemy import create_engine
import os
import time, datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options as ChromeOptions



class Infections(db.Model):
    __tablename__ = 'us_infections'

    index = db.Column(db.Integer, primary_key=True)
    combined_key = db.Column(db.String())
    date = db.Column(db.String())
    country_region = db.Column(db.String())
    cases = db.Column(db.Integer())
    province_state = db.Column(db.String())

    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
        }


class Data():
    us_deaths = None
    engine = None
    scraped_usa_total = []
    scraped_states_dict = {}

    def run_query(self, query):
       return pd.read_sql(query, con=self.engine)

    def init_selenium_driver(self):

        #Able to work on the heroku dyno and local system server
        chrome_bin = os.environ.get('GOOGLE_CHROME_SHIM', None)
        options = ChromeOptions()
        options.binary_location = chrome_bin
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(executable_path='chromedriver', chrome_options=options)

        #Scrap info cards will only be displayed if elements are found
        try:
            driver.get("https://www.worldometers.info/coronavirus/country/us/")
            tbody = driver.find_element_by_tag_name("tbody")
            #Grab just the first total row
            for row in tbody.find_elements_by_tag_name("tr"):
                cells = row.find_elements_by_tag_name("td")
                for cell in cells:
                    self.scraped_usa_total.append(cell.text)
                break
            #Grab every row for all states
            for row in tbody.find_elements_by_tag_name("tr"):
                cells = row.find_elements_by_tag_name("td")
                state_row = []
                for cell in cells:
                    state_row.append(cell.text)
                self.scraped_states_dict[state_row[0]] = state_row
            #Grab provinces
            tbody = driver.find_element_by_xpath("//*[@id='usa_table_countries_today']/tbody[2]")
            for row in tbody.find_elements_by_tag_name("tr"):
                cells = row.find_elements_by_tag_name("td")
                state_row = []
                for cell in cells:
                    state_row.append(cell.text)
                self.scraped_states_dict[state_row[0]] = state_row
            driver.close()

        except NoSuchElementException:
            self.scraped_usa_total = None
    def __init__(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])
        self.init_selenium_driver()

    def get_scraped_usa_total(self):
        return self.scraped_usa_total

    def get_scraped_states_dict(self):
        return self.scraped_states_dict

    #Desc: Groups cases by day then selects rows for last day of each month
    #Output: Dataframe
    def get_monthly_totals(self, df):
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df = df.iloc[df.reset_index().groupby(pd.to_datetime(df['date']).dt.to_period('M'))['index'].idxmax()]
        return df

    #Desc: Groups cases by day
    #Output: Dataframe
    def get_daily_totals(self, df):
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        return df

    def get_states(self):
        states_df = self.run_query('SELECT * FROM \"states\" ORDER BY province_state;')
        return states_df.province_state.unique()
   
    #Desc: Filters df rows by state
    #Updated Desc: Selects state table
    #Output: Dataframe
    def get_by_state(self, state):
        states_df = self.run_query('SELECT * FROM \"'+state+'\";')
        return states_df

    def get_us_total_infections(self):
        return self.run_query('SELECT * FROM \"us total\";')

    def add_month_name_column(self, df):
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df['month_name'] = df['day'].apply(lambda x: x.strftime('%b'))
        return df

    def add_day_name_column(self, df):
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df['day_name'] = df['day'].apply(lambda x: x.strftime('%b %d'))
        return df

    #Desc: Converts df to bootstrap compatible html table
    #Output: HTML table converted DataFrame
    def df_to_html(self, df):
        return df.to_html(index=False, classes=["table-bordered", "table-striped", "table-hover", "table-dark"])

    #Desc: Maps get_monthly_totals to each state
    #Output: List of [[States], [Dataframes]]
    def get_monthly_totals_by_state(self):
        all_province_states = self.get_states()
        monthly_province_state_dfs = []
        states = []
        for province_state in all_province_states:
            state_df = self.get_by_state(province_state)
            state_monthly_total_df = self.get_monthly_totals(state_df)
            state_monthly_total_df = self.add_month_name_column(state_monthly_total_df)
            state_monthly_total_df = state_monthly_total_df[['cases', 'month_name']]
            monthly_province_state_dfs.append(state_monthly_total_df)
            states.append(province_state)
        return [states, monthly_province_state_dfs]


    #Desc: Maps get_monthly_totals to each state
    #Output: List of [[States], [Dataframes]]
    def get_daily_totals_by_state(self):
        all_province_states = self.get_states()
        monthly_province_state_dfs = []
        states = []
        for province_state in all_province_states:
            state_df = self.get_by_state(province_state)
            state_monthly_total_df = self.get_daily_totals(state_df)
            state_monthly_total_df = self.add_day_name_column(state_monthly_total_df)
            state_monthly_total_df = state_monthly_total_df[['cases', 'day_name']]
            monthly_province_state_dfs.append(state_monthly_total_df)
            states.append(province_state)
        return [states, monthly_province_state_dfs]
