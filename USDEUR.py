import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
import datetime
from datetime import date, timedelta

today = date.today()

d1 = today.strftime("%Y-%m-%d")
end_date = d1
d2 = date.today() - timedelta(days=730)
d1 = d2.strftime("%Y-%m-%d")
start_date = d2

data = yf.download('EUR=X',
                   start=start_date,
                   end=end_date,
                   progress=False)

data["Date"] = data.index
data = data[["Date", "Open", "High", "Low", "Close", "Adj Close"]]
data.reset_index(drop=True, inplace=True)
print(data.head())

print(data.shape)

import plotly.graph_objects as go
figure = go.Figure(data=go.Candlestick(x=data["Date"],
                                       open=data["Open"],
                                       high=data["High"],
                                       low=data["Low"],
                                       close=data["Close"]))
figure.update_layout(title="USD-EUR Parity Analysis",
                     xaxis_rangeslider_visible=False)
figure.show()

correlation = data.corr()
print(correlation["Open"].sort_values(ascending=False))

from autots import AutoTS
model = AutoTS(forecast_length=10, frequency='infer', ensemble='simple')
model = model.fit(data, date_col='Date', value_col='Close', id_col='None')
prediction = model.predict()
forecast = prediction.forecast
print(forecast)