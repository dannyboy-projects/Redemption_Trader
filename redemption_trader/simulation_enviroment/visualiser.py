import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime, timedelta
# import datetime as dt


def create_interactive_visualiser(df, start_date = None, end_date = None):
    if pd.api.types.is_datetime64_any_dtype(df.index):
        pass
    else:
        df.index = pd.to_datetime(df.index)

    start_date = shift_timestamp(start_date, -5)
    end_date   = shift_timestamp(end_date, +5)

    df = df[(df.index >= start_date)& (df.index < end_date)]

    fig = go.Figure(data = [go.Candlestick(x = df.index,\
                                          open = df['open'],\
                                          high = df['high'],\
                                          low  = df['low'],\
                                          close= df['close'])])
    # fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


def shift_timestamp(timestamp, shift):

    t = pd.to_datetime(timestamp)
    DelTime = timedelta(minutes=shift)
    tz_off = (t + DelTime).strftime("%z")
    t = (t + DelTime).strftime("%Y-%m-%d %H:%M:%S")
    tz_off_format = tz_off[:3] + ':' + tz_off[3:]
    t = t + tz_off_format

    return t


def create_basic_visualiser(df,start_date = None, end_date = None):
    if pd.api.types.is_datetime64_any_dtype(df.index):
        pass
    else:
        df.index = pd.to_datetime(df.index)

    start_date = shift_datetime(start_date, -20)
    end_date   = pd.to_datetime(end_date, +5)

    df = df[(df.index >= start_date)& (df.index < end_date)]

    mpf.plot(df, type='candle', style = 'charles')
    plt.show()


def TradeLog_visualiser(df):
    df = df.reset_index()
    df = df.rename(columns = {'index': 'tradeID'})
    fig = go.Figure(data = [go.Table(header = dict(values = list(df.columns),align = 'center'),\
                                     cells=dict(values = [df[c].round(4) for c in df.columns],align = 'center'))])


    fig.show()




