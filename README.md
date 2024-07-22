# Redemption_Trader
Algo trading simulation and trading code base

---
### Overview
Brief overvew of the main components built here to develop aglorithmic trading strategies.

**Infrastructure**
- strategy objects :white_check_mark:
- simulation enviroment :white_check_mark:
- data pull and pre-processing :white_check_mark:
- live trading enviroment :red_circle:

**ML models Explored**
- Decision Tree (clf) :orange_diamond:
- Random Forest (clf) :orange_diamond:

The overall apporach here was to build strategy objects that behaved in the same manner whether they were being tested in simulation (backtest) capacity or in a live trading enviroment. To that end, a dynamically assing class was created, inheriting an order managemnt system, a data subscription object, and the individaul strategy (`Pipband`)inteself woth a custom `__init__` function.

`strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})`

Once the stragey is fully developped, the strat object can be instantiated using a live trading enviroment with mirrored functionality i.e. `Live_OMS`, `Live_data_subscription`

This allows seamless migration from development (simulation) to live trading - assuming the parent classes have been built correctly and with mirrored method names and attributes. 







