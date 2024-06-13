import pandas as pd

class SimDataSubscription:
   
    # def __init__(self, mode, items, fields, adapter=""):
    def __init__(self):
        print('hello sim data subscription')
        # self.item_names = items
        # self._items_map = {}
        # self.field_names = fields
        # self.adapter = adapter
        # self.mode = mode
        # self.snapshot = "true"
        self.listeners = []

        # self.epic = items[0].replace("CHART:","").replace(":5MINUTE","")
    def data_hello():
        print('hello from data')



    def add_listener(self,a):
        print('add hello from listener')
        self.listeners.append(a)



    def notifyupdate(self,line_entry):

        # print(str(line_entry)+"notifyupdate")

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
        #set hist data class varible in all strats so only needs to be set once
        
        # self.subscriptions[1].hist_data = self.OMS_LookUpBidAsk  #previously used for tradelog OMS
        for subkey in self.subscriptions:

            # #needs to be fixed 
            
            # epic = self.subscriptions[subkey].epic
            # cols = [epic+".open_bid",epic+".open_ask",epic+".high_bid",epic+".high_ask",epic+".low_bid",epic+".low_ask",epic+".close_bid",epic+".close_ask"]
            
            # data_entry = pd.DataFrame(self.OMS_LookUpBidAsk,columns=cols) # being created every single time mistake
            # # print(data_entry.loc[time])

            # find data for that specific strategy/instrument
            d = self.data_subscriptions[self.subscriptions[subkey].instrument].loc[time]
            # update time in OMS
            self.subscriptions[subkey].time = time
            #update current_candle in OMS
            self.subscriptions[subkey].current_candle = d
            # print(d.name, 'this is d')
            #feed current candle to strategy itself
            self.subscriptions[subkey].notifyupdate(d)#feed candle here
            self.subscriptions[subkey].update_positions()
        
            # self.subscriptions[subkey].update_positions(self.subscriptions[subkey].curr_candle_data)












