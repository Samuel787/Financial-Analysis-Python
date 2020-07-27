import bs4 as bs
import datetime as dt
import os
import pandas as pd
import pandas_datareader.data as web
import pickle
import requests
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import style

style.use('ggplot')

## Creates a pickle file with the s&p 500 companies web scraped from wikipedia
def save_sp500_tickers():
    resp = requests.get('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    soup = bs.BeautifulSoup(resp.text)
    table = soup.find('table', {'class': 'wikitable sortable'})
    tickers = []
    for row in table.findAll('tr') [1:]:
        ticker = row.findAll('td')[0].text
        ticker = ticker[0: len(ticker)-1]
        tickers.append(ticker)
    
    with open("sp500tickers.pickle", "wb") as f:
        pickle.dump(tickers, f, protocol=pickle.HIGHEST_PROTOCOL)
    print(tickers)
    return tickers

## pulls historical stock data from the pickle file or yahoo if file doesnt eixsts
## for the first 'NUM' companies mentioned in the S&P 500 listing
## creates csv files for the stocks from the pickle file
def get_data_from_yahoo(reload_sp500=False, NUM = 30):
    if reload_sp500:
        tickers = save_sp500_tickers()
    else:
        with open("sp500tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists('stock_dfs'):
        os.makedirs('stock_dfs')
    
    start = dt.datetime(2000,1,1)
    end = dt.datetime(2016,12,31)

    ## only retrieves first 30 tickers
    for i in range(NUM):
        ticker = tickers[i]
        print(ticker)
        if not os.path.exists('stock_dfs/{}.csv'.format(ticker)):
            try:
                df = web.DataReader(ticker.replace('.','-'), 'yahoo', start, end)
                df.to_csv('stock_dfs/{}.csv'.format(ticker))
            except Exception as ex:
                print('Error:', ex)
        else:
            print('Already have {}'.format(ticker))

## combines the stock data for the first NUM companies from their individual csv files
## into one csv file
def compile_data(NUM = 30):
    with open('sp500tickers.pickle', 'rb') as f:
        tickers = pickle.load(f)

    main_df = pd.DataFrame()
    new_tickers = tickers[0:NUM]
    for count, ticker in enumerate(new_tickers):
        df = pd.read_csv('stock_dfs/{}.csv'.format(ticker))
        df.set_index('Date', inplace=True)

        df.rename(columns = {'Adj Close': ticker}, inplace=True)
        df.drop(['Open', 'High', 'Low', 'Close', 'Volume'], 1, inplace=True)

        if main_df.empty:
            main_df = df
        else:
            main_df = main_df.join(df, how='outer')

        if count% 10 == 0:
            print(count)

    print(main_df.head())
    main_df.to_csv('sp500_joined_closes.csv')

## draws a heatmap to show correlation between stocks
def visualize_data():
    df = pd.read_csv('sp500_joined_closes.csv')
    # df['AES'].plot()
    # plt.show()

    df_corr = df.corr()
    print(df_corr.head())

    data = df_corr.values
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    heatmap = ax.pcolor(data, cmap=plt.cm.RdYlGn)
    fig.colorbar(heatmap)
    ax.set_xticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.set_yticks(np.arange(data.shape[1]) + 0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()

    column_labels = df_corr.columns
    row_labels = df_corr.index

    ax.set_xticklabels(column_labels)
    ax.set_yticklabels(row_labels)

    plt.xticks(rotation = 90)
    heatmap.set_clim(-1,1)
    plt.tight_layout()
    plt.show()


# save_sp500_tickers()


# get_data_from_yahoo()


# compile_data()

visualize_data()
