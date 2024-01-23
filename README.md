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

after that, run the `quantitative_momentum_strategy.py` on your machine to initiate the strategy.


## FYI: the Json response object returned from IEX Cloud Stock API
API request url: `https://cloud.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols=AAPL&token=[Your Token]`

API response
`{
  "AAPL": {
    "stats": {
      "companyName": "Apple Inc",
      "marketcap": 2961880797760,
      "week52high": 199.62,
      "week52low": 136.77,
      "week52highSplitAdjustOnly": 199.62,
      "week52lowSplitAdjustOnly": 137.9,
      "week52change": 0.400920149160406,
      "sharesOutstanding": 15461896000,
      "float": 0,
      "avg10Volume": 64957303,
      "avg30Volume": 54541764,
      "day200MovingAvg": 183.55,
      "day50MovingAvg": 190.71,
      "employees": 164000,
      "ttmEPS": 6.13,
      "ttmDividendRate": 0.9465536932059656,
      "dividendYield": 0.004941290943860752,
      "nextDividendDate": "",
      "exDividendDate": "2023-11-10",
      "nextEarningsDate": "2024-02-01",
      "peRatio": 30.53642762781587,
      "beta": 1.1398697081299738,
      "maxChangePercent": 73.87492182614135,
      "year5ChangePercent": 4.110733447343917,
      "year2ChangePercent": 0.19765420829529967,
      "year1ChangePercent": 0.400920149160406,
      "ytdChangePercent": -0.005038175868695816,
      "month6ChangePercent": 0.003355342621022217,
      "month3ChangePercent": 0.11097256496283904,
      "month1ChangePercent": -0.01602629956852275,
      "day30ChangePercent": -0.010537190082644532,
      "day5ChangePercent": 0.03033562822719449
    },
    "quote": {
      "avgTotalVolume": 54541764,
      "calculationPrice": "close",
      "change": 2.33,
      "changePercent": 0.01216,
      "close": 193.89,
      "closeSource": "official",
      "closeTime": 1705957200036,
      "companyName": "Apple Inc",
      "currency": "USD",
      "delayedPrice": 193.85,
      "delayedPriceTime": 1705957196014,
      "extendedChange": 0.02,
      "extendedChangePercent": 0.0001,
      "extendedPrice": 193.91,
      "extendedPriceTime": 1705971598147,
      "high": 195.33,
      "highSource": "15 minute delayed price",
      "highTime": 1705957199989,
      "iexAskPrice": 0,
      "iexAskSize": 0,
      "iexBidPrice": 0,
      "iexBidSize": 0,
      "iexClose": 193.88,
      "iexCloseTime": 1705957199781,
      "iexLastUpdated": 1705957199781,
      "iexMarketPercent": 0.016341244861546537,
      "iexOpen": 192.39,
      "iexOpenTime": 1705933801016,
      "iexRealtimePrice": 193.88,
      "iexRealtimeSize": 1,
      "iexVolume": 982662,
      "lastTradeTime": 1705957199781,
      "latestPrice": 193.89,
      "latestSource": "Close",
      "latestTime": "January 22, 2024",
      "latestUpdate": 1705957200036,
      "latestVolume": 60133852,
      "low": 192.26,
      "lowSource": "15 minute delayed price",
      "lowTime": 1705933803782,
      "marketCap": 2997907015440,
      "oddLotDelayedPrice": 193.85,
      "oddLotDelayedPriceTime": 1705957196014,
      "open": 192.34,
      "openTime": 1705933800993,
      "openSource": "official",
      "peRatio": 31.63,
      "previousClose": 191.56,
      "previousVolume": 68902985,
      "primaryExchange": "NASDAQ",
      "symbol": "AAPL",
      "volume": 60133852,
      "week52High": 199.62,
      "week52Low": 136.77,
      "ytdChange": 0.007121824131304185,
      "isUSMarketOpen": false
    }
  }
}`