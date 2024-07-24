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
**Basic Thesis**

Around market opens it is believed that prices move more predctably close to whole numbers e.g. 128.0000. This 'law of round numbers' or perhaps 'lore of round numbers' could be attributed to traders being more likely to fill orders around price levels that are easier to type-in, or perform mental aritmetic with. Perhaps structured products with FX options bundled together cold also trigger at convient price levels. The pipband strategy aims to exploit these daily patterns - if they exist.


**Entry Signals**

A simple cross-over of any 5 minute candle with an integer price level is taken as an entry signal. If price moves from below to close above an integer value, that is a long entry. If price moves from above to close below an integer value that is a short entry. 

The next higher(lower) integer value is taken as the target exit for Long (short) positions respectively.

E.g.



These simple trading rules, which allow for mulitple positions to be open at once, are designed to capture all possible trades over the dataset (USDJPY<sup>(IS)</sup> Apr 2022 - May 2024). Essentially, it worth analysing whether any statistal edge appears or not, before refining trading rules or modelling price movements. Is there any evidence that price movement in the FX market aren't random around market open and round numbers?







