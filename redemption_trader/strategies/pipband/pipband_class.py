from .helpers import *
# has to be capital letter to start class name
class Pipband:
    def __init__(self,id):
        self.strat_ID    = id
        self.instrument = ''
        self.timestamp   =  0
        self.parameters = {'account_risk_per_trade':0.01, 'min_RewardRisk': 1.00, 'session_PnL':0.00}
        self.status     = 'standby'
        self.open_px    = 0
        self.close_px   = 0
        self.timestops  = {}
        self.dealref    = ''
        self.DT_model = load_DT_model('./redemption_trader/strategies/pipband/DT.joblib')
        print('strat init, strat_ID: ', self.strat_ID)

    def set_parameters(self,risk_per_trade,min_R):
        pass    

    def listen_and_operate(self,data):
        
        band = 0.5
        
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
            
            if (new_candle(self.timestamp,data.name) and dir) and (valid_hours(self.timestamp)) :# dir is non-zero = True
    
                T_px, SL_px = gen_targets(dir,self.close_px,band)
                risk_GBP = self.parameters['account_risk_per_trade']*self.account_balance
                
                size = position_size(dir, self.close_px, SL_px,risk_GBP)
                # size = 1

                # flag_DT_model = self.DT_model.predict(format_model_input(data,dir))
                # if self.DT_model.predict([]) #need to format input [opentime_fmt, ect...]
                flag_DT_model = 1
                if dir ==1 and flag_DT_model:
                    self.dealref = self.deal("BUY",SL_px, T_px, size,self.instrument)
                    self.status = 'open_position'
                elif dir == -1 and flag_DT_model:
                    self.dealref = self.deal("SELL",SL_px, T_px, size,self.instrument)
                    self.status = 'open_position'
                # 6 hour timestop comes from prelim.ipynb
                self.timestops[self.dealref] = calc_timestop(data.name,7)
                
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])
            
        elif self.status == 'fill_check':
            pass
        elif self.status == 'open_position':

            if self.check_for_trades(self.dealref) == 0:
                self.status = 'start_up'
                self.timestops.pop(self.dealref)

            elif end_of_week(data.name):
                self.close_deal(self.dealref)
                self.timestops.pop(self.dealref)
                self.status = 'start_up'

            closed = []
            for s in self.timestops:
                if timestop(data.name,self.timestops[s]):
                    self.close_deal(s)
                    closed.append(s)
            if closed != []: 
                [self.timestops.pop(c) for c in closed] 
                self.status = 'start_up'


            

            self.timestamp = data.name

            
