import statsmodels.api as sm
import pandas as pd
import matplotlib
import itertools


#Load data
df = pd.read_excel("datasets/store.xls")
furniture = df.loc[df['Category']=='Furniture']

print(furniture['Order Date'].min(), furniture['Order Date'].max())
furniture = furniture[['Order Date','Sales']]
print(furniture.head())
print(furniture.isnull().sum())

#Sum over sales for each day
furniture = furniture.groupby('Order Date')['Sales'].sum().reset_index()
furniture = furniture.set_index('Order Date')
print(furniture.head())

print('Indexing with Time Series Data')
#Resampling allows you to change the time intercal in a time series to something else
#<DataFrame or Series>.resample(arguments).<aggregate function>
y = furniture['Sales'].resample('MS').mean()

#Let's plot y
y.plot(figsize=(15, 6))
print('Time Series Decomposition')
#Time Series Decomposition allows decomposing the time series into trend, seasonality and noise
decomp = sm.tsa.seasonal_decompose(y, model='additive')
fig = decomp.plot()
   #matplotlib.pyplot.show()


print('ARIMA Forecasting')
#ARIMA stands for Autoregressive Integrated Moving Average and is a commonly used time series forecasting method
#Information in the past values of the time series can alone be used to predict the future values
#Notation is ARIMA(p, d, q) where p, d, q are trend, seasonality and noise respectively
# p is the order of the AR term
# q is the order of the MA term
# d is the number of differencing required to make the time series stationary
#If the ARIMA has a season component it becomes a Seasonal ARIMA or SARIMA

#Finding parameteres for SARIMA

#p, d, q params take any value between 0 and 2
p = d = q = range(0, 2)
#pdq will be all combinations of p, d, q triplets
pdq = list(itertools.product(p, d, q))
print(pdq)