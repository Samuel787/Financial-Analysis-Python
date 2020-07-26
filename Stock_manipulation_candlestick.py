import datetime as dt
import matplotlib.pyplot as plt 
from matplotlib import style
from mpl_finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import pandas_datareader.data as web


###   Viewing stock price data in python ###
style.use('ggplot')

start = dt.datetime(2000, 1, 1)
end = dt.datetime(2016, 12, 31)

df = web.DataReader('TSLA', 'yahoo', start, end)
print(df.head())

print("--------")

print(df.tail(10))

# df.to_csv('tsla.csv')

df2 = pd.read_csv('tsla.csv', parse_dates=True, index_col = 0)


### displaying csv data frame
# df2.plot()
# plt.show()

# df2['100ma'] = df2['Adj Close'].rolling(window = 100, min_periods = 0).mean()
print(df2.head())
print("--------")
print(df2.tail())


df_ohlc = df['Adj Close'].resample('10D').ohlc()
df_volume = df['Volume'].resample('10D').sum()

df_ohlc.reset_index(inplace = True)
df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)




ax1 = plt.subplot2grid((6, 1), (0,0), rowspan = 5, colspan = 1)
ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan = 1, colspan = 1, sharex=ax1)
ax1.xaxis_date()

candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
ax2.fill_between(df_volume.index.map(mdates.date2num), df_volume.values, 0)
plt.show()


# ax1.plot(df2.index, df['Adj Close'])
# # ax1.plot(df2.index, df['100ma'])
# ax2.bar(df2.index, df['Volume'])

plt.show()


############################################