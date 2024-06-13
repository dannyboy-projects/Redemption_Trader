from .helpers import *
# has to be capital letter to start class name
class Pipband:
    def __init__(self,id):
        self.strat_ID    = id
        self.instrument = ''
        self.timestamp   =  0
        self.parameters = {'account_risk_per_trade':0.00, 'min_RewardRisk': 1.00, 'session_PnL':0.00}
        self.status     = 'standby'
        self.open_px    = 0
        self.close_px   = 0
        self.dealref    = ''
        print('strat init, strat_ID: ', self.strat_ID)

    def set_parameters(self,risk_per_trade,min_R):
        pass    


    def listen_and_operate(self,data):
        
        
        # print('hello from listener')
        # print(str(item_update['open'])+" listen"+str(self.strat_ID))
        # data_received = item_update.to_dict()
        # data_received['time'] = item_update.name
        # dir,stop_loss,target_px,quantity,instrument):
        band = 1
        
        if self.status == 'standby':
           print('startup')
           self.status = 'start_up'
           self.timestamp = data.name

        elif self.status == 'start_up':
            self.status = 'scanning'
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            

        elif self.status == 'scanning':
            print('scanning')
            dir = entry_signal(self.open_px,self.close_px,band)
            if new_candle(self.timestamp,data.name) and dir:# dir is non-zero = True
                print('new candle')
                
                T_px, SL_px = gen_targets(dir,self.close_px,band)

                if dir ==1:
                    self.dealref = self.deal("BUY",SL_px, T_px, 1,self.instrument)
                    self.status = 'open_position'
                elif dir == -1:
                    self.dealref = self.deal("SELL",SL_px, T_px, 1,self.instrument)
                    self.status = 'open_position'
                
            
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            
            
        elif self.status == 'fill_check':
            pass
        elif self.status == 'open_position':
            if self.check_for_trades(self.dealref) == 0:
                self.status = 'start_up'
            
            
        

