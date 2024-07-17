from .helpers import *
# has to be capital letter to start class name
class Pipband:
    def __init__(self,id):
        self.strat_ID    = id
        self.instrument = ''
        self.timestamp   =  0
        self.parameters = {'account_risk_per_trade':0.05, 'min_RewardRisk': 1.00, 'session_PnL':0.00}
        self.status     = 'standby'
        self.open_px    = 0
        self.close_px   = 0
        self.dealref    = ''
        print('strat init, strat_ID: ', self.strat_ID)

    def set_parameters(self,risk_per_trade,min_R):
        pass    

    def listen_and_operate(self,data):
        
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
            
            dir = entry_signal(self.open_px,self.close_px,band)
            open_markets = get_open_markets(self.timestamp)

            if (new_candle(self.timestamp,data.name) and dir) and (open_markets['London'] or open_markets['NYC']):# dir is non-zero = True
    
                T_px, SL_px = gen_targets(dir,self.close_px,band)
                risk_GBP = self.parameters['account_risk_per_trade']*self.account_balance
                
                size = position_size(dir, self.close_px, SL_px,risk_GBP)

                if dir ==1:
                    self.dealref = self.deal("BUY",SL_px, T_px, size,self.instrument)
                    self.status = 'open_position'
                elif dir == -1:
                    self.dealref = self.deal("SELL",SL_px, T_px, size,self.instrument)
                    self.status = 'open_position'
                
            
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            
        elif self.status == 'fill_check':
            pass
        elif self.status == 'open_position':

            if end_of_week(self.timestamp):
                self.close_deal(self.dealref)
                self.status = 'start_up'

            if self.check_for_trades(self.dealref) == 0:
                self.status = 'start_up'

            self.timestamp = data.name
