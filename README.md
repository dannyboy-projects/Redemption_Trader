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
- Decision Tree (clf) :small_orange_diamond:
- Random Forest (clf) :small_orange_diamond:

The overall apporach here was to build strategy objects that behaved in the same manner whether they were being tested in simulation (backtest) capacity or in a live trading enviroment. To that end, a dynamically assing class was created, inheriting an order managemnt system, a data subscription object, and the individaul strategy (`Pipband`)inteself woth a custom `__init__` function.

`strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})`

Once the stragey is fully developped, the strat object can be instantiated using a live trading enviroment with mirrored functionality i.e. `Live_OMS`, `Live_data_subscription`

This allows seamless migration from development (simulation) to live trading - assuming the parent classes have been built correctly and with mirrored method names and attributes. 

### Pipband Strategy
**Basic Premise**

Essentially, around market opens it is believed that prices move more predctably around whole numbers e.g. 128.0000. This 'law of round numbers' or perhaps 'lore of round numbers' could be attributed to traders being more likely to fill orders around price levels that are easoer to type in, or perform mental aritmetic with. Coupled with daily increased volume at market opens around the world the pipband strategy aims to exploit these daily patterns - if they exist.

To begin with, a simple cross-over of any 5 minute candle with an integer price level is taken as an entry signal. If price moves from below to close above an integer value, that is a long entry. If price moves from above to close below an integer value that is a short entry. 

The next hihger(lower) integer value is taken as the target exit for Long (short) positions respectively. 


**First Steps**

Pullling 2 years worth of USDJPY data





