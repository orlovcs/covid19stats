from fbprophet import Prophet
import pandas as pd


#Load data
df = pd.read_excel("datasets/store.xls")
furniture = df.loc[df['Category']=='Furniture']
furniture = furniture[['Order Date','Sales']]

furniture_model = Prophet(interval_width=0.95)