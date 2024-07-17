import pandas as pd
import random
import string
from datetime import datetime, timedelta


class SimOrderMgmtSystem:
    account_balance = 100
    open_positions  = {}
    limit_orders    = {}
    trade_log       = pd.DataFrame(columns = ['strat_id','instrument', 'open_time', 'open_price','close_time', 'close_price','dir','size','PnL'])
    time       = ''
    current_candle = ''

    def __init__(self):
        print('oms init')

    def Login():
        print('login to oms')

    # def _add2open_positions(self, px, deal_ref):
    
    def deal(self,dir,stop_loss,target_px,quantity,instrument):
        print('the time is ', self.time) 
        deal_ref = self._create_dealref()
        
        # print('curr',self.current_candle['open'])

        if dir == "BUY":
            dir = 1
            open_px = self.current_candle['open_ask']   
        elif dir == "SELL":
            dir = -1
            open_px = self.current_candle['open_bid']
        else:
            print('error in dir')
        
        if self.strat_ID in  self.open_positions:
                self.open_positions[self.strat_ID][deal_ref] = {'instrument':instrument,\
                                                                'open_time': self.current_candle.name,\
                                                                'dir': dir, 'open_PX':open_px,'size':quantity,\
                                                                'target': target_px,'stoploss':stop_loss,\
                                                                'close_PX': 'N/A','close_time':'OPEN_TRADE'\
                                                                ,'status':'FILLED_N_OPEN'}
            # print(self.open_positions)
        else:
            self.open_positions[self.strat_ID] = {deal_ref: \
                {'instrument':instrument, 'open_time': self.current_candle.name\
             ,'dir': dir, 'open_PX':open_px,'size':quantity,'target': target_px,'stoploss':stop_loss,\
            'close_PX': 'N/A','close_time':'OPEN_TRADE','status':'FILLED_N_OPEN'}}

        print(self.open_positions)
        return deal_ref

    def close_deal(self,trade_ID):
        # check to see if SL or TP hit first
        self.update_positions()

        closed_pos =  []
        
        if trade_ID in self.open_positions[self.strat_ID]:

            self.open_positions[self.strat_ID][trade_ID]['status'] = "CLOSED"

            if int(self.open_positions[self.strat_ID][trade_ID]['dir']) == 1:
                open_px = self.current_candle['open_bid']  
                self.open_positions[self.strat_ID][trade_ID]['close_PX'] = open_px # of next candle when exit 
                self.open_positions[self.strat_ID][trade_ID]['close_time'] = self.current_candle.name
                closed_pos.append(trade_ID)
            elif int(self.open_positions[self.strat_ID][trade_ID]['dir']) == -1:
                open_px = self.current_candle['open_ask']
                self.open_positions[self.strat_ID][trade_ID]['close_PX'] = open_px
                self.open_positions[self.strat_ID][trade_ID]['close_time'] = self.current_candle.name
                closed_pos.append(trade_ID)

            self._closed_pos2tradeLog(self.strat_ID,trade_ID,self.open_positions[self.strat_ID][trade_ID] )
            self.open_positions[self.strat_ID].pop(trade_ID)

            

    def limit_order(self,dir,entry,stop_loss,target_px,quantity,cancel_time,epic):
        pass

    

    def close_limit_order(self,trade_ID):
        pass

    def check_for_trades(self,tradeID):
        if self.strat_ID in self.open_positions:
    
            if tradeID in self.open_positions[self.strat_ID]:
                status = self.open_positions[self.strat_ID][tradeID]['status']
                if status == "FILLED_N_OPEN":
                    status = 1
                else:
                    status = 0
            else:
                status = 0 
        else:
            status = 0
        return status
        

    def check_for_working_orders(self,trade_ID):
        pass

    def deal_entry_check(self, trade_ID):
        pass

        
    def _closed_pos2tradeLog(self, strat_id, trade_id, closed_pos):

        # adjust for trading on candle close
        open_time = pd.to_datetime(closed_pos['open_time'])
        DelTime = timedelta(minutes=5)
        tz_off = (open_time - DelTime).strftime("%z")
        open_time= (open_time - DelTime).strftime("%Y-%m-%d %H:%M:%S")

        # tz_off = open_time.strftime('%z')
        tz_off_format = tz_off[:3] + ':' + tz_off[3:]
        open_time = open_time + tz_off_format

        close_time = closed_pos['close_time']
        # close_time = pd.to_datetime(close_time + DelTime)

        print(closed_pos)
        PnL = closed_pos['dir']*closed_pos['size']*(closed_pos['close_PX'] - closed_pos['open_PX'])
        self.trade_log.loc[trade_id] = [strat_id,\
                                        closed_pos['instrument'],\
                                        open_time,\
                                        closed_pos['open_PX'],\
                                        close_time,\
                                        closed_pos['close_PX'],\
                                        closed_pos['dir'],\
                                        closed_pos['size'],\
                                        PnL]
        # update strat object local parametes
        self.parameters['session_PnL'] += PnL
        self.account_balance += PnL
        # print(self.parameters['session_PnL'])
        print(self.trade_log)
        print(self.account_balance)
        return 0
       
    def _filled_Limit2open_pos(self,filled_Limit):
        pass

    def update_positions(self):
       
        closed_pos = []
        if self.strat_ID in self.open_positions:
            for tradeID in self.open_positions[self.strat_ID]:
                
                # print('update_positions',float(self.open_positions[self.strat_ID][tradeID]['target']), self.current_candle['high_bid'])
                #     print(trade)
                # entry = self.open_positions[strat][tradeID]
                if int(self.open_positions[self.strat_ID][tradeID]['dir']) == 1:
                    if float(self.current_candle["high_bid"]) >= float(self.open_positions[self.strat_ID][tradeID]['target']):
                        self.open_positions[self.strat_ID][tradeID]['status'] = "CLOSED"
                        self.open_positions[self.strat_ID][tradeID]['close_PX'] = self.open_positions[self.strat_ID][tradeID]['target']
                        self.open_positions[self.strat_ID][tradeID]['close_time'] = self.current_candle.name
                        closed_pos.append(tradeID)
                    elif float(self.current_candle["low_bid"]) <= float(self.open_positions[self.strat_ID][tradeID]['stoploss']):
                        self.open_positions[self.strat_ID][tradeID]['status'] = "CLOSED"
                        self.open_positions[self.strat_ID][tradeID]['close_PX'] = self.open_positions[self.strat_ID][tradeID]['stoploss']
                        self.open_positions[self.strat_ID][tradeID]['close_time'] = self.current_candle.name
                        closed_pos.append(tradeID)
                elif int(self.open_positions[self.strat_ID][tradeID]['dir']) == -1:
                    if float(self.current_candle["low_ask"]) <= float(self.open_positions[self.strat_ID][tradeID]['target']):
                        self.open_positions[self.strat_ID][tradeID]['status'] = "CLOSED"
                        self.open_positions[self.strat_ID][tradeID]['close_PX'] = self.open_positions[self.strat_ID][tradeID]['target']
                        self.open_positions[self.strat_ID][tradeID]['close_time'] = self.current_candle.name
                        closed_pos.append(tradeID)
                    elif float(self.current_candle["high_ask"]) >= float(self.open_positions[self.strat_ID][tradeID]['stoploss']):
                        self.open_positions[self.strat_ID][tradeID]['status'] = "CLOSED"
                        self.open_positions[self.strat_ID][tradeID]['close_PX'] = self.open_positions[self.strat_ID][tradeID]['stoploss']
                        self.open_positions[self.strat_ID][tradeID]['close_time'] = self.current_candle.name
                        closed_pos.append(tradeID)

            if closed_pos != []:
                for c in closed_pos:
                    self._closed_pos2tradeLog(self.strat_ID,c,self.open_positions[self.strat_ID][c] )
                    self.open_positions[self.strat_ID].pop(c)

    def _create_dealref(self):
        rand_ref = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return rand_ref
