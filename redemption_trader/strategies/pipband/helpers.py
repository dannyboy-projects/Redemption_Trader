import math
import datetime, pytz
import time
import pandas as pd
import math as m
import joblib
from datetime import timedelta

def load_DT_model(DT_model_filename):
    return joblib.load(DT_model_filename)

def format_model_input(data,dir):
    df = pd.DataFrame(index = [0],columns = ['open_time_fmt','dir','percent2MA','percent_candle_size','parkinson_volatility'])
    df.loc[0,'open_time_fmt'] = pd.to_datetime(data.name).hour*12 + pd.to_datetime(data.name).minute
    df.loc[0,'dir'] = dir

    df.loc[0,'percent_candle_size'] = (midmarket(data['close_bid'],data['close_ask']) - midmarket(data['open_bid'],data['open_ask'])) \
        /midmarket(data['open_bid'],data['open_ask'])
    df['parkinson_volatility'] = data['parkinson_volatility']

    df.loc[0,'percent2MA'] = (df['open'] - df['open'].rolling(12).mean())

  
    return df.copy()

def get_R(entry, target, stoploss):
    return (target - stoploss)/(entry - stoploss)

def position_size(dir, entry,SL_px, risk_GBP):
    GBP_per_pt = dir*risk_GBP/(entry - SL_px)
    return GBP_per_pt

def entry_signal(open_px, close_px,band ):
    Lo, Hi = nearest_00levels(open_px,band)
    if Hi == Lo:
        dir = 0
    else:

        if close_px > Hi and open_px < Hi:
            dir = 1
        elif close_px < Lo and open_px > Lo:
            dir = -1
        else:
            dir = 0
    return dir

def new_candle(timestamp, time):
    if timestamp != time:
        return True
    else:
        return False

def midmarket(bid,ask):
    return 0.5*(bid+ask)
#------------------------------------------------
#   Strategy Specific
#------------------------------------------------
def nearest_00levels(px,band):
    HiLevel = band*( math.floor(px/band)+ 1 )
    LoLevel = band *( math.floor(px/band))
    return LoLevel, HiLevel


def gen_targets(dir,px,band):
    Lo,Hi = nearest_00levels(px,band)

    if dir ==1:
        T_px = Hi
        SL_px = Lo - band
    elif dir ==-1:
        T_px = Lo
        SL_px = Hi + band
    return T_px, SL_px


def end_of_week(utc):
    utc =pd.to_datetime(utc,utc = True).to_pydatetime()
    nyc = pytz.timezone('America/New_York')
    nyc_time = utc.astimezone(nyc)

    nyc_close_hrs = 17
    # print(nyc_time)
    # print(nyc_time.weekday())  
    if nyc_time.weekday() == 4 and nyc_time.hour >= nyc_close_hrs:
        return True
    else:
        return False

def valid_hours(t):
    t = pd.to_datetime(t).to_pydatetime()

    valid_hours = [8,15]

    if t.hour in (valid_hours):
        return True
    else:
        return False
    


def calc_timestop(open_time, t_stop):
    t = pd.to_datetime(open_time)
    DelTime = timedelta(hours = t_stop)
    tz_off = (t + DelTime).strftime("%z")
    t = (t + DelTime).strftime("%Y-%m-%d %H:%M:%S")
    tz_off_format = tz_off[:3] + ':' + tz_off[3:]
    t = t + tz_off_format
    return t


def get_open_markets(utc):
    Tokyo = False
    Sydney = False
    London = False
    NewYorkCity    = False
 
    utc =pd.to_datetime(utc,utc = True).to_pydatetime()



    jst = pytz.timezone('Asia/Tokyo')
    jst_time = utc.astimezone(jst)
    # dt.tz_convert()

    # Tokyo
    tokyo_open_hrs = 9
    tokyo_close_hrs = 18

    if (jst_time.hour >= tokyo_open_hrs) and (jst_time.hour < tokyo_close_hrs):
        Tokyo = True

    # aussie
    aussie = pytz.timezone('Australia/Sydney')
    aussie_time = utc.astimezone(aussie)

    sydney_open_hrs = 9
    sydney_close_hrs = 17

    if (aussie_time.hour >= sydney_open_hrs) and (aussie_time.hour < sydney_close_hrs):
        Sydney = True

    # London
    Ldn = pytz.timezone('Europe/London')
    Ldn_time = utc.astimezone(Ldn)

    Ldn_open_hrs = 8
    Ldn_close_hrs = 16
    Ldn_close_mins = 30

    if (Ldn_time.hour >= Ldn_open_hrs) and (Ldn_time.hour < Ldn_close_hrs) and (Ldn_time.minute < Ldn_close_mins):
        London = True
    
    # NYC
    nyc = pytz.timezone('America/New_York')
    nyc_time = utc.astimezone(nyc)

    nyc_open_hrs = 8
    nyc_close_hrs = 17

    if (nyc_time.hour >= nyc_open_hrs) and (nyc_time.hour < nyc_close_hrs):
        NewYorkCity = True

    return {'Tokyo':Tokyo, 'Sydney':Sydney, 'London':London, 'NYC':NewYorkCity}


def timestop(t, timestop):
    t = pd.to_datetime(t)
    timestop = pd.to_datetime(timestop)

    if t >= timestop:
        return True
    else: 
        return False

    


    

