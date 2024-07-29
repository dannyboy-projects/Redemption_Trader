from .helpers import *
import pandas as pd
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
        self.timestops  = {}
        self.aux_data = pd.DataFrame(columns = ['candle_size', 'percent_candle_size','parkinson_volatility'\
                                                ,'shortterm_momentum','momentum','longterm_momentum','extralongterm_momentum'\
                                                    ,'percent2MA_shortterm','percent2MA_longterm'])
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
# and valid_hours(self.timestamp)
            if ((new_candle(self.timestamp,data.name) and dir) ):# dir is non-zero = True
    
                T_px, SL_px = gen_targets(dir,self.close_px,band)
                risk_GBP = self.parameters['account_risk_per_trade']*self.account_balance
                
                size = position_size(dir, self.close_px, SL_px,risk_GBP)
                size =1

                if dir ==1:
                    self.dealref = self.deal("BUY",SL_px, T_px, size,self.instrument)
                    # self.status = 'open_position'
                elif dir == -1:
                    self.dealref = self.deal("SELL",SL_px, T_px, size,self.instrument)
                    # self.status = 'open_position'
                # self.timestops[self.dealref] = calc_timestop(data.name,40)

                # generate aux data for ML model
                candle_size = midmarket(data['close_bid'],data['close_ask']) - midmarket(data['open_bid'],data['open_ask'])
                self.aux_data.loc[self.dealref] = [candle_size,\
                                                   candle_size/midmarket(data['open_bid'],data['open_ask']),\
                                                   data['parkinson_volatility'],
                                                    data['shortterm_momentum'],data['momentum'],\
                                                    data['longterm_momentum'], data['extralongterm_momentum'],\
                                                    data['percent2MA_shortterm'], data['percent2MA_longterm'] ]

            # check timestops
            closed = []
            for s in self.timestops:
                if data.name >= self.timestops[s]:
                    self.close_deal(s)
                    closed.append(s)

            if closed != []: 
                [self.timestops.pop(c) for c in closed] 
                        
            self.timestamp = data.name
            self.open_px   = midmarket(data['open_bid'],data['open_ask'])
            self.close_px  = midmarket(data['close_bid'],data['close_ask'])

            


            
    





