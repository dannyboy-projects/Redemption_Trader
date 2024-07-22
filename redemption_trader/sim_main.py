import simulation_enviroment as sim_env
import strategies.strat_test as test
import strategies.pipband    as pipband
import pandas as pd



GlobalStreamObj = sim_env.StreamData_Sim()

def sim_init(self,id):
    print('custom_init')
    pipband.Pipband.__init__(self,id)
    sim_env.SimDataSubscription.__init__(self)
    sim_env.SimOrderMgmtSystem.__init__(self)

def sim_DataLabeller_init(self,id):
    print('custom_init')
    pipband.Pipband_DataLabeller.__init__(self,id)
    sim_env.SimDataSubscription.__init__(self)
    sim_env.SimOrderMgmtSystem.__init__(self)

# strat = type('SimStrat', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,test.Strat),{'__init__':sim_init})
strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})
data_labeller = type('pipband_DataLabeller', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband_DataLabeller),{'__init__':sim_DataLabeller_init})
s = strat(1)
t = data_labeller(2)


s.add_listener(s.listen_and_operate)
# t.add_listener(t.listen_and_operate)

GlobalStreamObj.Subscribe(s)
s.instrument = 'C:USDJPY'


usdjpy = pd.read_csv('./redemption_trader/processed_data/C:USDJPY_clean_OS.csv',index_col = 0)
print(usdjpy.head())
usdjpy_visualiser = usdjpy.copy()

# sim_env.create_interactive_visualiser(usdjpy.head())
# sim_env.create_basic_visualiser(usdjpy, start_datetime='2022-05-29 21:00:00+00:00', end_datetime='2022-05-30 21:00:00+00:00')
usdjpy = sim_env.add_parkinson_volatility(usdjpy,576)
usdjpy = sim_env.add_momentums(usdjpy)
print(usdjpy)


usdjpy = sim_env.midMarket2BidAsk(usdjpy,0.00005)
print(usdjpy)
GlobalStreamObj.load_data_subscription('C:USDJPY',usdjpy)

for i in range(len(usdjpy)):
    GlobalStreamObj.time_step(usdjpy.index.values[i])


# print(s.trade_log)
sim_env.TradeLog_visualiser(s.trade_log)

s.trade_log.to_csv('tradelog.csv')
# t.aux_data.to_csv('aux_data.csv')


print(s.account_balance)


# for t in s.trade_log.index:
#     sim_env.create_interactive_visualiser(usdjpy_visualiser, start_datetime=s.trade_log.loc[t]['open_time'], end_datetime=s.trade_log.loc[t]['close_time'])





















