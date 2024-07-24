import simulation_enviroment as sim_env
import strategies.strat_test as test
import strategies.pipband    as pipband
import pandas as pd


#----------------------------------------------------------------------
# Inputs
#----------------------------------------------------------------------

visualise_tradelog = True


#----------------------------------------------------------------------



# custom __init__ used for dynamic class creation
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


GlobalStreamObj = sim_env.StreamData_Sim()


#----------------------------------------------------------------------
# Build list of strategy objects
#----------------------------------------------------------------------

# dynamic creation of classes
# strat = type('SimStrat', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,test.Strat),{'__init__':sim_init})
strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})
data_labeller = type('pipband_DataLabeller', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband_DataLabeller),{'__init__':sim_DataLabeller_init})

# create strat objs, arg is strat id
s = strat(1)
t = data_labeller(2)

# populate list
strategies = [t]

for strat in strategies:
    strat.add_listener(strat.listen_and_operate)
    GlobalStreamObj.Subscribe(strat)
    strat.instrument = 'C:USDJPY'

#----------------------------------------------------------------------
# Load processed data
#----------------------------------------------------------------------


usdjpy = pd.read_csv('./redemption_trader/processed_data/C:USDJPY_clean_OS.csv',index_col = 0)

usdjpy_visualiser = usdjpy.copy()

# sim_env.create_interactive_visualiser(usdjpy.head())
# sim_env.create_basic_visualiser(usdjpy, start_datetime='2022-05-29 21:00:00+00:00', end_datetime='2022-05-30 21:00:00+00:00')
# create auxialry data, moving averages, 
usdjpy = sim_env.add_parkinson_volatility(usdjpy,576)
usdjpy = sim_env.add_momentums(usdjpy)

# spread modelling
usdjpy = sim_env.midMarket2BidAsk(usdjpy,0.00005)
GlobalStreamObj.load_data_subscription('C:USDJPY',usdjpy)



#----------------------------------------------------------------------
# Main loop
#----------------------------------------------------------------------
for i in range(len(usdjpy)):
    GlobalStreamObj.time_step(usdjpy.index.values[i])



sim_env.TradeLog_visualiser(s.trade_log)
strategies[0].trade_log.to_csv('tradelog.csv')

# t.aux_data.to_csv('aux_data.csv')
print(strategies[0].trade_log)
print(strategies[0].account_balance)


if visualise_tradelog:
    for t in strategies[0].trade_log.index:
        print('dir: ', strategies[0].trade_log.loc[t,'dir'], 'PnL: ', strategies[0].trade_log.loc[t,'PnL'], 'dealref: ', t)
        open_time = strategies[0].trade_log.loc[t]['open_time']
        close_time = strategies[0].trade_log.loc[t]['close_time']
        sim_env.create_interactive_visualiser(usdjpy_visualiser, start_date=open_time, end_date=close_time)
        input('')




















