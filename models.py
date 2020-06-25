"""Interacts with database."""
import os
from sqlalchemy import create_engine
import pandas as pd

class Data():
    """Data class for pulling db tables."""
    us_deaths = None
    engine = None
    driver = None
    scraped_states_dict = {}

    def run_query(self, query):
        """Return pandas SQL query."""
        return pd.read_sql(query, con=self.engine)

    def __init__(self):
        """Create the engine."""
        self.engine = create_engine(os.environ['DATABASE_URL'])

    #Load in data from scrapped dashboard table
    def get_scraped_usa_total(self):
        """Get main scrapped data."""
        scrap_total_df = self.run_query('SELECT * FROM \"us total scrap\";')
        scrap_total_df_list = scrap_total_df['values'].values.tolist()
        return scrap_total_df_list

    #Load in data from scrapped state table
    def get_scraped_state(self, state):
        """Get state scrapped data."""
        scrap_total_df = self.run_query('SELECT * FROM \"'+state+' scrap\";')
        scrap_total_df_list = scrap_total_df['values'].values.tolist()
        return scrap_total_df_list

    #Desc: Groups cases by day then selects rows for last day of each month
    #Output: Dataframe
    def get_monthly_totals(self, df):
        """Return monthly totals."""
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df = df.iloc[df.reset_index().groupby(pd.to_datetime(df['date']).dt.to_period('M'))['index'].idxmax()]
        return df

    #Desc: Groups cases by day
    #Output: Dataframe
    def get_daily_totals(self, df):
        """Return daily totals."""
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        return df

    def get_states(self):
        """Return all states."""
        states_df = self.run_query('SELECT * FROM \"states\" ORDER BY province_state;')
        return states_df.province_state.unique()

    #Desc: Filters df rows by state
    #Updated Desc: Selects state table
    #Output: Dataframe
    def get_by_state(self, state):
        """Filters by state."""
        states_df = self.run_query('SELECT * FROM \"'+state+'\";')
        return states_df

    def get_us_total_infections(self):
        """Total infections."""
        return self.run_query('SELECT * FROM \"us total\";')

    def add_month_name_column(self, df):
        """Adds month name column to df table."""
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df['month_name'] = df['day'].apply(lambda x: x.strftime('%b'))
        return df

    def add_day_name_column(self, df):
        """Adds day name column to df table."""
        df['day'] = pd.to_datetime(df['date']).dt.to_period('D')
        df['day_name'] = df['day'].apply(lambda x: x.strftime('%b %d'))
        return df

    #Desc: Converts df to bootstrap compatible html table
    #Output: HTML table converted DataFrame
    def df_to_html(self, df):
        """Return formatted HTML df table."""
        return df.to_html(index=False, classes=["table-bordered", "table-striped", "table-hover", "table-dark"])

    #Desc: Maps get_monthly_totals to each state
    #Output: List of [[States], [Dataframes]]
    def get_monthly_totals_by_state(self):
        """Monthly totals per state."""
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
        """Daily totals per state."""
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
