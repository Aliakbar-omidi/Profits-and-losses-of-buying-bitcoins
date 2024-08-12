
import pandas as pd
import yfinance as yf
from persiantools.jdatetime import JalaliDateTime, JalaliDate


df = yf.download('BTC-USD', start="2019-01-01", end="2024-08-05")

df.reset_index(inplace=True)

df["Date"] = pd.to_datetime(df["Date"])

df["JalaliDate"] = df["Date"].apply(lambda x: JalaliDate(x))
df["JalaliWeekDay"] = df["Date"].apply(lambda d: JalaliDate(d).isoweekday())

sun_list = df.where(df["JalaliWeekDay"] == 1)
wed_list = df.where(df["JalaliWeekDay"] == 5)


print(sun_list.dropna())