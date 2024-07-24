import pandas as pd

class SimDataSubscription:
   
    def __init__(self):
        print('hello sim data subscription')
        self.listeners = []

    def data_hello():
        print('hello from data')

    def add_listener(self,a):
        print('add hello from listener')
        self.listeners.append(a)

    def notifyupdate(self,line_entry):

        for strat_block in self.listeners:
            strat_block(line_entry)




class StreamData_Sim():

    subscriptions = {}
    curr_subkey = 0
    data_subscriptions = {}
    # time = 0

    def __init__(self):
        pass

    def Subscribe(self,sub_obj):
        self.curr_subkey += 1
        self.subscriptions[self.curr_subkey] = sub_obj


    def load_data_subscription(self,instrument,df):
        self.data_subscriptions[instrument] = df

    def create_BidAsk(o,h,l,c,spread):
        pass

    def time_step(self,time):

        for subkey in self.subscriptions:

            # find data for that specific strategy/instrument
            d = self.data_subscriptions[self.subscriptions[subkey].instrument].loc[time]

            # update time in OMS
            self.subscriptions[subkey].time = time

            #update current_candle in OMS
            self.subscriptions[subkey].current_candle = d
           
            #feed current candle to strategy itself
            self.subscriptions[subkey].notifyupdate(d)      #feed candle here
            self.subscriptions[subkey].update_positions()
        












