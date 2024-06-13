from .helpers import *

class Strat:
    def __init__(self,id):
        self.strat_ID    = id
        self.instrument = ''
        self.timestamp   =  0
        self.parameters = {'account_risk_per_trade':0.00, 'min_RewardRisk': 1.00, 'session_PnL':0.00}
        self.status     = 'standby'
        print('strat init, strat_ID: ', self.strat_ID)




    def hello():
        print('hello')
        # R_filter()

    def set_parameters(self):
        pass    


    def listen_and_operate(self,item_update):
        
        # print('hello from listener')
        # print(str(item_update['open'])+" listen"+str(self.strat_ID))
        # data_received = item_update.to_dict()
        # data_received['time'] = item_update.name
        # dir,stop_loss,target_px,quantity,instrument):
        
        if self.status == 'standby':
            self.deal("SELL",130.0,126.8,1,self.instrument)
            self.status = 'scanning'
            # pass
        elif self.status == 'start_up':
            pass
        elif self.status == 'scanning':
            pass
        elif self.status == 'fill_check':
            pass
        elif self.status == 'open_position':
            pass  
        

