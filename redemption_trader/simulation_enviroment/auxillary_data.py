import pandas as pd
import math as m

def parkinson_volatility(hi,Lo):
    variance = (1.0/(4.0*m.log(2)))*(m.log(hi/Lo))**2
    return m.sqrt(variance)



def add_parkinson_volatility(df,t_as_int):
    #t as number of candles lookback period
    df['parkinson_volatility'] = df['close'].rolling(t_as_int).apply(lambda x: parkinson_volatility(x.max(),x.min()) ,raw = True)
    return df

def add_momentums(df):
    #t as number of candles lookback period
    df['shortterm_momentum'] = df['open'].rolling(window = 3).mean() - df['open'].rolling(window = 12).mean()
    df['momentum'] = df['open'].rolling(window = 12).mean() - df['open'].rolling(window = 36).mean()
    df['longterm_momentum'] = df['open'].rolling(window = 76).mean() - df['open'].rolling(window = 288).mean()    
    df['extralongterm_momentum'] = df['open'].rolling(window = 288).mean() - df['open'].rolling(window = 1440).mean()
    df['percent2MA_shortterm'] = (df['open'] - df['open'].rolling(window = 12).mean())/df['open'].rolling(window = 12).mean()
    df['percent2MA_longterm'] = (df['open'] - df['open'].rolling(window = 288).mean())/df['open'].rolling(window = 288).mean()


    return df
