import statsmodels.api as sm
import pandas as pd
import matplotlib
import itertools
import warnings
import numpy as np


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
#fig = decomp.plot()
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

seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
print(seasonal_pdq)
#ignore extra info
warnings.filterwarnings("ignore")
aic_arr = []
#find the best triplet
for param in pdq:
   for param_seasonal in seasonal_pdq:
      try:
         mod = sm.tsa.statespace.SARIMAX(y, 
         order=param,
         seasonal_order=param_seasonal,
         enforce_stationarity=False,
         enforce_invertibility=False)

         results = mod.fit()
         #print('ARIMA - {}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
         aic_arr.append([param, param_seasonal, results.aic])
      except:
         continue

#Sort by AIC value
aic_arr.sort(key = lambda x :x[2])
print(aic_arr)
#Find triplet with lowest AIC value, assume it is SARIMAX(1, 1, 1)x(1, 1, 1, 12)
#Plug the triplet into the new SARIMAX model
mod = sm.tsa.statespace.SARIMAX(y,
order=(1,1,1),
seasonal_order=(1,1,0,12),
enforce_invertibility=False,
enforce_stationarity=False)

results = mod.fit()

print(results.summary().tables[1])

#Investigate any violations
   #results.plot_diagnostics(figsize=(15, 12))
   #matplotlib.pyplot.show()

#Run the prediction from the end of the dataset - 2017-01-01
pred = results.get_prediction(start=pd.to_datetime('2017-01-01'), dynamic=False)
pred_ci = pred.conf_int()

ax = y['2014':].plot(label='observed')
pred.predicted_mean.plot(ax=ax, label='One-step ahead Forecast', alpha=0.7)

ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color = 'k', alpha=0.2)

ax.set_xlabel('Date')

matplotlib.pyplot.legend()
matplotlib.pyplot.show()

#Use mean squared error to quantify accuracy
y_forecasted = pred.predicted_mean
y_truth=y['2016-01-01':]

#Compute mean squared
mse=((y_forecasted - y_truth) ** 2).mean()
print('Mean Squared Error of foreasts is {}'.format(round(mse, 2)))
print('Root Mean Squared Error of forecasts is {}'.format(round(np.sqrt(mse), 2)))



#Run the prediction from the end of the dataset - 2017-01-01
pred_uc = results.get_forecast(steps=100)
pred_ci = pred.conf_int()

ax = y.plot(label='observed')
pred_uc.predicted_mean.plot(ax=ax, label='Forecast', alpha=0.7)

ax.fill_between(pred_ci.index,
               pred_ci.iloc[:, 0],
               pred_ci.iloc[:, 1], color = 'k', alpha=0.2)

ax.set_xlabel('Date')
ax.set_ylabel('Sales')

matplotlib.pyplot.legend()
matplotlib.pyplot.show()
