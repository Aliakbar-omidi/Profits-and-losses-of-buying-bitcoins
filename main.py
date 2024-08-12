
import pandas as pd
import yfinance as yf
from persiantools.jdatetime import JalaliDateTime, JalaliDate


df = yf.download('BTC-USD', start="2019-01-01", end="2024-08-05")

df.reset_index(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["JalaliDate"] = df["Date"].apply(lambda x: JalaliDate(x))
df["JalaliWeekDay"] = df["Date"].apply(lambda d: JalaliDate(d).isoweekday())

sun_list = df[df["JalaliWeekDay"] == 1]
wed_list = df[df["JalaliWeekDay"] == 5]

sun_open = sun_list["Open"]
wed_close = sun_list["Close"]

df["Benefit"] = wed_close - sun_open

# print(sun_list.dropna())
# print(sun_open)
# print(wed_close)
# print(df["Benefit"])

print(df["Benefit"].dropna())