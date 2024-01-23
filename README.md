# quantitative_momentum_strategy
in this algorithmic trading project, we build an investing strategy that selects the 50 stocks with the highest price momentum. From there, we will calculate recommended trades for an equal-weight portfolio of these 50 stocks.


## how does this work in high level
in order to find the 50 best stock to invest, we first get all S&P500 stock tickers and fetch their status information from IEX Cloud stock API. from API response, we extract the data of latestPrice, year1ChangePercent, month6ChangePercent, month3ChangePercent, month1ChangePercent parameter for each stock. 

with those information, we can cacluate the percentile of each ChangePercent (1 year, 6 month, 3 month, 1 month) for every stock ,and then take an average among these four caculated percentile to calculate the high-quality-momentum (HQM) score. the stock with higher HQM score is better.

after HQM scores are calculated, we select the 50 stocks with the highest HQM score and form our portfolio. next step, user will enter the value of the portfolio. for example: $1,000,000. the program will use this portfolio value to evenly distribute to these 50 stocks and calculate the number of shares need to buy.

the final result including all the metric data will be generated to an excel file called quant_momentum_strategy_result.xlsx 


## reqirement to run program
you need to install python 3 and the following libraries if you have not already:
* numpy
* pandas
* requests

after that, run the quantitative_momentum_strategy.py on your machine to initiate the strategy.