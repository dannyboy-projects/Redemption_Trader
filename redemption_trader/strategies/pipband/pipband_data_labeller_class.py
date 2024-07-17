from .helpers import *
# has to be capital letter to start class name
class Pipband_DataLabeller:
    def __init__(self,id):
        self.strat_ID    = id
        self.instrument = ''
        self.timestamp   =  0
        self.parameters = {'account_risk_per_trade':0.05, 'min_RewardRisk': 1.00, 'session_PnL':0.00}
        self.status     = 'start_up'
        self.open_px    = 0
        self.close_px   = 0
        self.dealref    = ''
        print('strat init, strat_ID: ', self.strat_ID)

    def set_parameters(self,risk_per_trade,min_R):
        pass    

    def listen_and_operate(self,data):
        
        band = 1
        if self.status == 'start_up':

            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            self.status    = 'gen_signal'

        elif self.status == 'gen_signal':
         
            dir = entry_signal(self.open_px,self.close_px,band)
            open_markets = get_open_markets(self.timestamp)

            if (new_candle(self.timestamp,data.name) and dir):# dir is non-zero = True
    
                T_px, SL_px = gen_targets(dir,self.close_px,band)
                # risk_GBP = self.parameters['account_risk_per_trade']*self.account_balance
                
                # size = position_size(dir, self.close_px, SL_px,risk_GBP)

                if dir ==1:
                    self.dealref = self.deal("BUY",SL_px, T_px, 1,self.instrument)
                    # self.status = 'open_position'
                elif dir == -1:
                    self.dealref = self.deal("SELL",SL_px, T_px, 1,self.instrument)
                    # self.status = 'open_position'
            
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            
    





