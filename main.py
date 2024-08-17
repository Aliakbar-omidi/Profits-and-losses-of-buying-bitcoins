import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

btc = yf.download('BTC-USD', period='max', start='2019-01-01')
df = pd.DataFrame(btc)
df.drop(columns=['Volume', 'Adj Close', 'Low'], inplace=True)
df.reset_index(inplace=True)
df['DayWeek'] = df['Date'].dt.dayofweek
df = df[df['DayWeek'].isin([5, 2])]
df.reset_index(inplace=True)
if df.loc[0, 'DayWeek'] == 2:
    df.drop(index=0, inplace=True)
df['new_close'] = df['Close'].shift(-1)
df['new_hight'] = df['High'].shift(-1)
df = df[df['DayWeek'].isin([5])]
df.drop(columns=['index', 'DayWeek'], inplace=True)
df['start_point'] = df['end_point'] = 1000.0
df.to_csv('BTC.csv', index=False)

df = pd.read_csv('BTC.csv')
ratio = df['new_close'] / df['Open']
df['end_point'] = df['start_point'] * ratio.cumprod()
df['start_point'] = df['end_point'].shift(1)
df['btc'] = df['start_point'] / df['Open']
df.reset_index(drop=True, inplace=True)
df.to_csv("BTC(open-close).csv", index=False)

df = pd.read_csv('BTC(open-close).csv')
fig = make_subplots(rows=1, cols=2)
df['text'] = 'wallet : ' + df['start_point'].round().astype(str) + '$'
fig.add_trace(go.Scatter(x=df['Date'], y=df['start_point'], text=df['text'], name='$'), row=1, col=1)
df['text'] = 'wallet : ' + df['btc'].round(2).astype(str) + 'BTC'
fig.add_trace(go.Scatter(x=df['Date'], y=df['btc'], text=df['text'], name='BTC'), row=1, col=2)

fig.update_layout(width=1300, height=500, )
fig.show()
