import pandas as pd



def midMarket2BidAsk(df,percent_spread):
    new_cols = []
    old_cols = []
    for c in df.columns:
        if c in ['open','high','low','close']:
            bid = c+'_bid'
            ask = c+'_ask'
            new_cols.append(bid)
            new_cols.append(ask)
        else:
            old_cols.append(c)

    dg = pd.DataFrame(index = df.index,columns=new_cols)
    

    dg['open_bid'] = df['open']*(1.0 - 0.5*percent_spread)
    dg['open_ask'] = df['open']*(1.0 + 0.5*percent_spread)
    dg['high_bid'] = df['high']*(1.0 - 0.5*percent_spread)
    dg['high_ask'] = df['high']*(1.0 + 0.5*percent_spread)
    dg['low_bid']  = df['low']*(1.0 - 0.5*percent_spread)
    dg['low_ask']  = df['low']*(1.0 + 0.5*percent_spread)
    dg['close_bid']  = df['close']*(1.0 - 0.5*percent_spread)
    dg['close_ask']  = df['close']*(1.0 + 0.5*percent_spread)

    #cols that dont need spread modelling pass through

    for d in old_cols:
        dg[d] = df[d]

    return dg

