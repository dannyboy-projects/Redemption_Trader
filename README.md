# Redemption_Trader
Algo trading simulation and trading code base

---
# Overview
Brief overvew of the main components built here to develop algorithmic trading strategies.

# Infrastructure
- **Strategy objects** :white_check_mark:
- **simulation enviroment** :white_check_mark:
- **Data pull and pre-processing** :white_check_mark:
- Live trading enviroment :red_circle:

The overall approach was to build strategy objects that behaved in the same manner whether they were being tested in a simulation (backtest) capacity, or in a live trading enviroment. To that end, dynamically asigned classes are created, inheriting an order managemnt system, a data subscription object, and the individaul strategy (`Pipband`) itself with a custom `__init__` function. e.g. For more details on using the `type()` function wiht 3 inputs read here

e.g.

`strat = type('pipband', (sim_env.SimOrderMgmtSystem,sim_env.SimDataSubscription,pipband.Pipband),{'__init__':sim_init})`

Once a strategey is fully developed, the same strat class can be used to instantiate a live trading version of the same strategy using a live trading enviroment with mirrored functionality to the simualtion enviroment i.e. `Live_OMS`, `Live_data_subscription`

`strat = type('pipband', (Live_env.SimOrderMgmtSystem,Live_env.LiveDataSubscription,pipband.Pipband),{'__init__':Live_init})`

This allows seamless migration from development (simulation) to live trading - assuming the parent classes have been built with mirrored method names and attributes. 



# Pipband Strategy
### Basic Trade Idea

Around market opens it is believed that prices move more predictably close to whole numbers e.g. 128.0000 adn especially around market opens and closes when trading activity picks up. This 'law of round numbers' or perhaps 'lore of round numbers' could be attributed to traders being more likely to fill orders around price levels that are easier to type-in, or perform mental aritmetic with. Perhaps structured products with FX options bundled together cold also trigger at convenient price levels. The pipband strategy aims to exploit these daily patterns - if they exist. 

USDJPY was taken as a starting point. The BoJ is the largest holder of US Treasuries and the associated FX hedging is theorised to produce repeating patterns in USDJPY price movements. (https://www.statista.com/chart/31941/largest-foreign-holders-of-us-treasury-bonds/)


## Entry Signals

A simple cross-over of any 5 minute candle with an integer price level is taken as an entry signal. If price moves from below to close above an integer value, that is a long entry. If price moves from above to close below an integer value that is a short entry. 

The next higher(lower) integer value is taken as the target exit for Long (short) positions respectively, wiht the lower (higher) integer levels being taken as the stop loss level.

E.g.


![long_entry](./strategy_exploration/pipband_exploration/figures/newplot.png)



These simple trading rules, which allow for mulitple positions to be open at once, are designed to capture all possible trades over the In-Sample dataset: USDJPY<sup>(IS)</sup> Apr 2022 - May 2023. 

A constant position size of 1 was used for all trades, in order to calculate PnL. 


Essentially, it worth analysing whether any statistal edge appears or not, before refining trading rules or modelling price movements. Is there any evidence that price movement in the FX market aren't random around market open/close and round numbers?

## All Entry Signals (IS)

Perhaps as evidence in the origianl thesis, spikes in the frequency in entry signals are seen near or around market opens as illustrated in following graph.

![no_trades_per_hour1](./strategy_exploration/pipband_exploration/figures/trade_freq_IS.png)

Next, aggregating the PnL, win rates, and calculating the expected value per entry hour allows us to single out where the most succesful entry signals are coming from. 

For given hour h:

(1) Filter out all trades with entry signals coming from that hour of day i.e. all trades from 21:00 - 21:55 --> 21 bucket

(2) Calculate PnL, win rate, and EV as follows

$\text{PnL(h)} = \sum\limits_{i}^H{\text{PnL}_i}$ 

Where H is the number of trades in hour h

$\text{win rate(h)} = \frac{W(h)}{L(h)}$ 

Where W(h), L(h) are the number of winning/losing trades in hour h

$\text{EV(h)} = \frac{\text{no. trades in hour h}}{\text{total no. of trades}} \;\;\; \text{PnL(h)}$ 

A spread of 0.5 bps was used, roughly 80-100 pips throughout the simulation.


Thus, plotting all three values: 


![no_trades_per_hour1](./strategy_exploration/pipband_exploration/figures/wr_EV_IS.png)


The most succesful entry signal exist as far to the top right corner as possible, and 4 hours stand out as the best. Namely, the hour (UTC) of 13, 15, 19, 21

These hours serve as more evidence of the signficance of US open and close, and the repeating patterns that statsitaclly seem to appear. 

Furthermore, considering the average time in trade of winners and losers might help us implement a time stop as well as favour winning trades if possible


|Hour| win rate (%) |Median Time in Trade Wins(hr) |Median Time in Trade Losses (hr) |
|----|-------------|:-------------------:|---------------------|
|13| 59.3 | 22.3 | 23|
|15| 57.5 | 21.4 | 22.3 |
|19| 61.1 | 23.6 | 28.9|
|21| 58.6 |39.5 | 32.9|


So clearly a timestop can't disguish between winning and losing trades, but a histogram of all trades shows the majority of trades taking less than 40 hours to complete.




## Results

Compiling the trading rules derived on the In-Sample data:

(1) Only trade entry signals generated in the hours of [13,15,19,21]

(2) 40 hr timestop

Rules to be tested:
(3) % account risk per trade (5%) - instead of flat position size

(4) One trade open versus many trades open at once

Now using Out-of-Sample data (2023-05-31 to 2024-04-27), let's test the one-open vs multiple trades approach


### One-Trade Open

![equity_curve_1](./strategy_exploration/pipband_exploration/figures/one_trade_open_equity_curve.png)


***IS results***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-7.98| 0.31 |3.80|
|Weekly|-11.20|2.18|6.08|
|Monthly|-10.30|9.45|13.37|
***


Sharpe <sup>(IS)</sup> = 2.37




***OS Results***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-5.05| 0.14 |3.57|
|Weekly|-8.97|0.99|4.44|
|Monthly|-10.22|4.29|7.86|
***



Sharpe <sup>(OS)</sup> = 1.75 



***Joint IS-OS***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-7.98| 0.22 |3.71|
|Weekly|-11.20|1.55|5.43|
|Monthly|-10.30|6.70|11.33|
***



Sharpe <sup>(IS + OS)</sup> = 1.95 <br />

RFR = 4%<br />
$\text{Annulised Monthly} \sigma_p = \sqrt{12} \sigma_{p,monthly}$<br />

$\text{Sharpe} = \frac{\text{Annualised return \%} - RFR\%}{\text{Annulised Monthly}\; \sigma_p}$<br />




### Multiple Trades Open

![equity_curve_2](./strategy_exploration/pipband_exploration/figures/multiple_trades_equity_curve.png)



***IS results***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-11.46| 0.39 |4.20|
|Weekly|-11.00|2.69|7.41|
|Monthly|-18.68|11.69|17.12|


Sharpe <sup>(IS)</sup> = 2.30




***OS Results***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-10.12| 0.18 |3.24|
|Weekly|-11.73|1.27|6.14|
|Monthly|-11.59|5.49|12.26|
***

Sharpe <sup>(OS)</sup> = 1.46 



***Joint IS-OS***
| |max. Draw Down (%) | Cumulative Growth Rate | Volatility of Returns (%)|
|---|---|---|---|
|Daily|-11.46| 0.28 |3.85|
|Weekly|-11.73|1.95|6.88|
|Monthly|-18.67|8.43|15.19|
***

Sharpe <sup>(IS + OS)</sup> = 1.85<br />

RFR = 4%<br />


$\text{Annulised Monthly} \sigma_p = \sqrt{12} \sigma_{p,monthly}$<br />

$\text{Sharpe} = \frac{\text{Annualised return \%} - RFR\%}{\text{Annulised Monthly}\; \sigma_p}$<br />

## Conclusions 


- **The one-trade open approach has a better Sharpe ratio of 1.75 in OS testing compared to 1.46 in the multi-trade approach**

- **Sharpe ratio not affect by % account risk per trade, but max drawdown is. One-trade approach has moderately lower drawdowns than multi-trade approach**

-**Multitrade approach can have up to 10 trades open at once, may not be margin efficient in context of wider portfolio**

## Future Work

- Investigate other currency pairs, ideally unrelated to US and JPY markets. i.e. EURGBP, CHFGBP, AUDNZD

- Evaluate basket of currency trading strategies (Draw Down, Sharpe) Hopefully Sharpe can be imporved further 

- Can ML help predict succesful trades given backtesting data?
Decision Trees, regression, What variables to measure at trade entry that could predict win/loss?

- Build Live Trading enviroment (margin calculations, hosting, Broker APIs)


# How to Run

## Data Pull - Polygon.api

## Simulations

`sim_main.py` is where the strategy objects are created and 


