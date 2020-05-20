from app import db
import pandas as pd
from sqlalchemy import create_engine
import os
import time, datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    author = db.Column(db.String())
    published = db.Column(db.String())

    def __init__(self, name, author, published):
        self.name = name
        self.author = author
        self.published = published

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'author': self.author,
            'published':self.published
        }

class Infections(db.Model):
    __tablename__ = 'us_infections'

    id = db.Column(db.Integer, primary_key=True)
    combined_key = db.Column(db.String())
    date = db.Column(db.String())
    cases = db.Column(db.Integer())
    country_region = db.Column(db.String())
    province_state = db.Column(db.String())

    def __init__(self, index):
        self.id = id

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
        }
    #CUSTOM FUNC
    def test():
        return "Hi"

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
        df = df.groupby(['day','date'])['cases'].sum().reset_index()
        df = df.iloc[df.reset_index().groupby(pd.to_datetime(df['date']).dt.to_period('M'))['index'].idxmax()]
        return df

    def get_states(self, df):
        return df.province_state.unique()
    #Desc: Filters df rows by state
    #Output: Dataframe
    def get_by_state(self, df, state):
        return df.loc[df['province_state'] == state]

    def get_us_infections(self):
        return self.us_infections

    def add_month_name_column(self, df):
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df['month_name'] = df['day'].apply(lambda x: x.strftime('%b'))
        return df
    #Desc: Converts df to bootstrap compatible html table
    #Output: HTML table converted DataFrame
    def df_to_html(self, df):
        return df.to_html(index=False, classes=["table-bordered", "table-striped", "table-hover", "table-dark"])

    #Desc: Maps get_monthly_totals to each state
    #Output: List of [[States], [Dataframes]]
    def get_monthly_totals_by_state(self):
        all_province_states = self.get_states(self.us_infections)
        months = []
        monthly_province_state_dfs = []
        for province_state in all_province_states:
            state_df = self.get_by_state(self.us_infections, province_state)
            state_monthly_total_df = self.get_monthly_totals(state_df)
            monthly_province_state_dfs.append(state_monthly_total_df)
            months.append(months)
        return [months, monthly_province_state_dfs]
