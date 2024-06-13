import pandas as pd
from os import listdir
import datetime, pytz

def aggregate_polygon_csvs(in_folder,target_folder,name):
    files = listdir(in_folder)
    dg = []

    for f in files:
        g = pd.read_csv(in_folder+f, index_col = 0)
        dg.append(g)

    df = pd.concat(dg, ignore_index=False)
    df = df.sort_index()
    df.to_csv(target_folder+name)

def clean_fx_data(df,from_utc):
    # remember data pulled in UTC
    # need to find PST including DLS
    # clear all entries before Sunday 5 pm and after Friday 5 pm 
    # re-upload csv/
    # FX market runs from 5 pm ET/EST (NY time) Sunday to 5 pm Friday 
    # df in by default in UTC
    # eastern_time = pytz.timezone('US/Eastern')
    # eastern_time.localize()
    if from_utc:
        df['timestamp'] = pd.to_datetime(df.index, utc = True)
        df['timestamp'] = df['timestamp'].dt.tz_convert('America/New_York')
        mask = (df['timestamp'].dt.dayofweek == 6) & (df['timestamp'].dt.hour<17)
        df = df[~mask]

        mask = (df['timestamp'].dt.dayofweek == 4) & (df['timestamp'].dt.hour>17)
        df= df[~mask]
        df = df.drop('timestamp', axis=1)

        return df
    





    

if __name__ == "__main__":
    file = 'USDJPY_2.csv'
    aggregate_polygon_csvs('../data_pull_tmp/', '../data/', file)
    usdjpy =  pd.read_csv('../data/'+file, index_col = 0)
    usdjpy = clean_fx_data(usdjpy,True)
    usdjpy.to_csv(file+'_clean'+'.csv')
    # usdjpy = pd.read_csv('../data/USDJPY_Eastern_Time.csv', index_col = 0)
    # usdjpy['timestamp'] = pd.to_datetime(usdjpy.index, utc = True)
    # usdjpy['timestamp'] = usdjpy['timestamp'].dt.tz_convert('America/New_York')

    # mask = (usdjpy['timestamp'].dt.dayofweek == 6) & (usdjpy['timestamp'].dt.hour<17)
    # usdjpy = usdjpy[~mask]

    # mask = (usdjpy['timestamp'].dt.dayofweek == 4) & (usdjpy['timestamp'].dt.hour>17)
    # usdjpy = usdjpy[~mask]

    # usdjpy.to_csv('USDJPY_cleaned.csv')

    # usdjpy = usdjpy.drop(usdjpy.loc[])    



    # print(usdjpy.index)
    # print(pd.api.types.is_datetime64_any_dtype(usdjpy.index))
    # usdjpy.index = pd.to_datetime(usdjpy.index, utc = True)
    # usdjpy.index = usdjpy.index.tz_convert('America/New_York')
    # usdjpy = usdjpy[usdjpy.index]
    # usdjpy.to_csv('../data/USDJPY_Eastern_Time.csv')
