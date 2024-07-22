import requests as rq
import pandas as pd
from polygon import RESTClient
import datetime
import time
import math
from helpers import *
import os

MAX_AGGS = 50000


def weekdays_between(start_date, end_date):
    """Generate all weekdays between start_date and end_date"""
    day = start_date
    while day <= end_date:
        if day.weekday() < 5:  # 0-4 denotes Monday to Friday
            yield day
        day += datetime.timedelta(days=1)


def get_aggs_for_symbol_and_date(symbols,start,end,resolution, multiplier):

    client = RESTClient(trace=True,api_key = "PR16BoGg0F9ZoGj9cvTkOSdkpolU97nA")  # Uses POLYGON_API_KEY environment variable
    aggs = []
    
    for s in symbols:
        data = pd.DataFrame(columns=['open','high','low','close'])
        os.makedirs('./data_tmp/'+str(s), exist_ok = True)

        for a in client.list_aggs(
            s,
            multiplier,
            resolution,
            start,
            end,
            limit=50000,
        ):
            # row = [a.timestamp,a.open]
            data.loc[datetime.datetime.fromtimestamp(a.timestamp/1000,datetime.timezone(datetime.timedelta(hours = 0)))] = [a.open, a.high, a.low, a.close]
            # aggs.append(a)# a is agg class, in-built onject to polygon .open, .close,.timestamp ect..

        print('finish pulling '+str(s))
    # start = datetime.datetime.strftime(start_date,"%Y-%m-%d")
        data.to_csv('./data_tmp/'+str(s)+'/'+str(s)+'_'+start+'.csv')


def is_within_data_lim(start, end,resolution):
    start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date   = datetime.datetime.strptime(end, '%Y-%m-%d')

    delta = end_date - start_date

    if resolution == 'minute':
        delta = delta.total_seconds()/60
       
    elif resolution == 'day':
        delta = delta.days
        
    return delta <= MAX_AGGS


def get_hist_data(instruments, start, end,params= None):
    # start_date = datetime.datetime.strptime(start, "%Y-%m-%d")
    end_date   = datetime.datetime.strptime(end, '%Y-%m-%d')
    
    if params['source'] == 'polygon':
        Friday = get_Friday(start)
        final_Friday = datetime.datetime.strptime(Friday,'%Y-%m-%d') + datetime.timedelta(days = 5*7)

        if is_within_data_lim(start, end,params['resolution']):
            print('within data lim')
            get_aggs_for_symbol_and_date(instruments,start,end,params['resolution'],params['multiplier'])
            return end_date
        else:
            print('max data')
            get_aggs_for_symbol_and_date(instruments,start,datetime.datetime.strftime(final_Friday,"%Y-%m-%d")\
                                                                                            ,params['resolution'],params['multiplier'])
            return final_Friday

    


def get_Friday(start_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    day_of_week = start_date.isoweekday()
    print(day_of_week)

        # start_date = start_date + datetime.timedelta(days = 7 - day_of_week + 1)
    friday      = start_date - datetime.timedelta(days = ((day_of_week-1))) + datetime.timedelta(days = (4))
    return friday.strftime("%Y-%m-%d")    


def Monday_2_fxSunday_open(start_date):
    start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    day_of_week = start_date.isoweekday()
    Monday = start_date - datetime.timedelta(days= day_of_week - 1)

    if Monday.isoweekday() != 1:
        print('error not Monday start')
    else:
        return (Monday - datetime.timedelta(hours = 3)).strftime("%Y-%m-%d")
    


if __name__== '__main__':

    poly_params = {'source':'polygon','resolution':'minute','multiplier':5}

    pause = 12 #seconds since 5 api calls per min
    Monday = "2024-04-29"
    date_fmt = "%Y-%m-%d"
    Sunday_open = Monday_2_fxSunday_open(Monday)
    end = get_Friday('2024-07-19')
    instrument = ["C:USDJPY"]
    
    delta = (datetime.datetime.strptime(end,date_fmt)  - datetime.datetime.strptime(Monday,date_fmt)).total_seconds()/60

    no_data_requests = math.floor(delta/MAX_AGGS) + 1

    for dreq in range(no_data_requests):
        final_Friday = get_hist_data(instrument, Sunday_open, end, poly_params)
        print("pulled ", Sunday_open, " to ", datetime.datetime.strftime(final_Friday,date_fmt))
        Monday = final_Friday + datetime.timedelta(days = 3)
        Sunday_open = Monday_2_fxSunday_open(datetime.datetime.strftime(Monday,date_fmt))
        print(Sunday_open,type(Sunday_open))
        time.sleep(pause)

    for i in instrument:

        aggregate_polygon_csvs('./data_tmp/'+str(i)+'/', './', str(i)+'_consolidated.csv')
        df =  pd.read_csv(str(i)+'_consolidated.csv', index_col = 0)
        df = clean_fx_data(df,True)
        df.to_csv(str(i)+'_clean.csv')

    








    
        


    










    