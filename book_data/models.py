from app import db
import pandas as pd
from sqlalchemy import create_engine
import os
import time, datetime


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
    us_infections = None
    us_deaths = None
    engine = None

    def run_query(self, query):
       return pd.read_sql(query, con=self.engine)

    def __init__(self):
        self.engine = create_engine(os.environ['DATABASE_URL'])
        self.us_infections = self.run_query('SELECT * FROM us_infections;')

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
        states_df = self.run_query('SELECT * FROM \"states\";')
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
