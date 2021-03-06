# StockAlg
Quantitative trading algorithm using mean reversion

NOTE: this is my very first trading alg, meant only to see how it might be done.
The next version will implement machine learning and a different kind of strategy...

This program is used to test and implement a quantatiative trading algorithm 
that uses the idea of reversion to the mean. Reversion to the mean is the idea
that stocks have an inherent price, and the fluctuations in the market are 
people over-valuing and under-valuing the price. 

Suppose we want to know when to buy and sell a stock. We keep track of the 
running means with two different lengths of time: one short (m1) and one long (m2). 
m1 follows the whims of the price a bit more closely, and m2 is a bit more stable.
When m1 becomes lower than m2, the stock is undervalued and we buy. When m1 becomes
greater than m2, the stock is overvalued and we sell (or short, if that's an option).

The question then is: "what is the optimum values of m1 and m2?" and "how to do we pick
which stocks to put our money into?" The first depends on the company (in particular, 
the company's volatility) while the second depends on weights that will need to be
carefully optimized. 
