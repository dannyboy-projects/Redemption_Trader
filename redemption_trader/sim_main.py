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
    


# strat = type('SimStrat', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,test.Strat),{'__init__':sim_init})
strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})

s = strat(1)
# t = strat(2)

s.add_listener(s.listen_and_operate)

GlobalStreamObj.Subscribe(s)

s.instrument = 'C:USDJPY'





usdjpy = pd.read_csv('./sim_data_mgmt/polygon_client/C:USDJPY_clean.csv',index_col = 0)
print(usdjpy.head())

usdjpy = sim_env.midMarket2BidAsk(usdjpy,0.005)

# print(usdjpy)

GlobalStreamObj.load_data_subscription('C:USDJPY',usdjpy)


for i in range(len(usdjpy)):
    GlobalStreamObj.time_step(usdjpy.index.values[i])

print(s.trade_log)


s.trade_log.to_csv('tradelog.csv')
print(s.account_balance)





















