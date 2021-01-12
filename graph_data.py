# In this file we plot the results for specified companies given by the user

# Import libraries
import matplotlib.pyplot as plt 
from matplotlib import style
import matplotlib.dates as mdates
from mpl_finance import candlestick_ohlc
import yfinance as yf
import pandas as pd 
import os
import numpy as np
import datetime as dt
import shutil
from textwrap import wrap
plt.style.use("ggplot")


def add_stock_data():
    path="C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\stockdata"
    if os.path.exists(path):
        shutil.rmtree("stockdata")
    paths = os.listdir("sentiment_dfs")
    full_path = 'C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\sentiment_dfs\\'
    start = dt.datetime(2016, 1, 1)
    end = dt.datetime.now()
    stock_not_exist = []

    for path in paths:
        ticker = path.replace(".csv","")
        df = yf.download(ticker, start, end)
        if not os.path.exists("stockdata"):
            os.makedirs("stockdata")

        if df.empty:
            stock_not_exist.append(path)
        else:
            df.to_csv(os.path.join("stockdata", path))

    for path in stock_not_exist:
        path = full_path + path
        os.remove(path)

def graph_data():
    # Read stock and analysis data 
    user = input("Pick a stock ticker that had recent filings activity to visualize: ")
    stock = pd.read_csv("C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\stockdata\\"+ user.upper() +".csv", parse_dates=True, index_col=0)
    df = pd.read_csv("C:\\Users\\Kaiz Nanji\\Desktop\\AlgorithmicStockBot\\sentiment_dfs\\"+ user.upper() +".csv", parse_dates=True, index_col=3)
    df = df[::-1]

    # Define axis data for candlestick graph
    df_ohlc = stock['Adj Close'].resample('10D').ohlc()
    df_sentiment = df['SentimentQDAP']
    df_ohlc.reset_index(inplace=True)
    df_ohlc['Date'] = df_ohlc['Date'].map(mdates.date2num)
    df_cosine = df['cosine similarity']

    # depict visualization
    ax1 = plt.subplot2grid((7,1),(0,0),rowspan=4,colspan=1)
    plt.ylabel('Price', size=20)
    plt.title(user.upper()+" Analysis", size=30)
    ax2 = plt.subplot2grid((7,1),(4,0),rowspan=2,colspan=1, sharex=ax1)
    plt.ylabel('\n'.join(wrap('Difference in Reporting Language', 17)), size=10)   
    ax3 = plt.subplot2grid((7,1),(6,0),rowspan=1,colspan=1, sharex=ax1)
    plt.ylabel('Sentiment', size=10)
    ax1.xaxis_date()
    candlestick_ohlc(ax1, df_ohlc.values, width=2, colorup='g')
    ax2.fill_between(df_cosine.index.map(mdates.date2num), df_cosine.values, color='b')
    ax3.fill_between(df_sentiment.index.map(mdates.date2num), df_sentiment.values, color='g')


    # Show graph
    plt.show()




