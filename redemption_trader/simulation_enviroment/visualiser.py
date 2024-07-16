import plotly.graph_objects as go
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
# import datetime as dt


def create_interactive_visualiser(df, start_datetime = None, end_datetime = None):
    if pd.api.types.is_datetime64_any_dtype(df.index):
        pass
    else:
        df.index = pd.to_datetime(df.index)

    df = df[(df.index >= pd.to_datetime(start_datetime))& (df.index < pd.to_datetime(end_datetime))]
    fig = go.Figure(data = [go.Candlestick(x = df.index,\
                                          open = df['open'],\
                                          high = df['high'],\
                                          low  = df['low'],\
                                          close= df['close'])])
    # fig.update_layout(xaxis_rangeslider_visible=False)
    fig.show()


def create_basic_visualiser(df,start_datetime = None, end_datetime = None):
    if pd.api.types.is_datetime64_any_dtype(df.index):
        pass
    else:
        df.index = pd.to_datetime(df.index)

    df = df[(df.index >= pd.to_datetime(start_datetime))& (df.index < pd.to_datetime(end_datetime))]
    # print(pd.to_datetime(end_datetime))
    # print(df.index < pd.to_datetime(end_datetime))
    # df = df[(df.index < pd.to_datetime(end_datetime)) ]
    mpf.plot(df, type='candle', style = 'charles')
    plt.show()


def TradeLog_visualiser(df):
    df = df.reset_index()
    df = df.rename(columns = {'index': 'tradeID'})
    fig = go.Figure(data = [go.Table(header = dict(values = list(df.columns),align = 'center'),\
                                     cells=dict(values = [df[c].round(4) for c in df.columns],align = 'center'))])


    fig.show()




