import numpy as np #The Numpy numerical computing library
import pandas as pd #The Pandas data science library
import requests #The requests library for HTTP requests in Python
import xlsxwriter #The XlsxWriter libarary for 
import math #The Python math module
from scipy import stats #The SciPy stats module
from statistics import mean
from IEX_API_secrets import IEX_CLOUD_API_TOKEN


# chunk: split a list into evenly sized chunks
def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n] 

# portfolio_input: accept an input from user for the portfolio size
def portfolio_input():
    portfolio_size = input("Enter the value of your portfolio:")

    try:
        val = float(portfolio_size)
        return val
    except ValueError:
        print("That's not a number! \n Try again:")
        portfolio_input() 

# read all ticker of S&P500
stocks = pd.read_csv('sp_500_stocks.csv')

# split tickers into multiple lists, each list contains at most 100 tickers. this is for batch api call later
symbol_groups = list(chunks(stocks['Ticker'], 100))
symbol_strings = []
for i in range(0, len(symbol_groups)):
    symbol_strings.append(','.join(symbol_groups[i]))
    #print(symbol_strings[i])

# define column names for hqm (high quality momentum) dataframe
hqm_columns = [
                'Ticker', 
                'Price', 
                'Number of Shares to Buy', 
                'One-Year Price Return', 
                'One-Year Return Percentile',
                'Six-Month Price Return',
                'Six-Month Return Percentile',
                'Three-Month Price Return',
                'Three-Month Return Percentile',
                'One-Month Price Return',
                'One-Month Return Percentile',
                'HQM Score'
                ]

hqm_dataframe = pd.DataFrame(columns = hqm_columns)

# call data api to fetch market information for all tickers
for symbol_string in symbol_strings:
    batch_api_call_url = f'https://cloud.iexapis.com/stable/stock/market/batch/?types=stats,quote&symbols={symbol_string}&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):
        if symbol in data:
            hqm_dataframe = hqm_dataframe._append(
                                            pd.Series([symbol, 
                                                    data[symbol]['quote']['latestPrice'],
                                                    'N/A',
                                                    data[symbol]['stats']['year1ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month6ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month3ChangePercent'],
                                                    'N/A',
                                                    data[symbol]['stats']['month1ChangePercent'],
                                                    'N/A',
                                                    'N/A'
                                                    ], 
                                                    index = hqm_columns), 
                                                    ignore_index = True)

time_periods = [
                'One-Year',
                'Six-Month',
                'Three-Month',
                'One-Month'
                ]

# calculate Return Percentile based on Price Return for each time frame      
for time_period in time_periods:
    hqm_dataframe[f'{time_period} Return Percentile'] = hqm_dataframe[f'{time_period} Price Return'].rank(pct=True)

# calclulate HQM score for each stock (take average among all 4 Return Percentile)
for row in hqm_dataframe.index:
    momentum_percentiles = []
    for time_period in time_periods:
        momentum_percentiles.append(hqm_dataframe.loc[row, f'{time_period} Return Percentile'])
    hqm_dataframe.loc[row, 'HQM Score'] = mean(momentum_percentiles)


# Selecting the 50 Best Momentum Stocks
hqm_dataframe = hqm_dataframe.sort_values(by = 'HQM Score', ascending = False)
hqm_dataframe = hqm_dataframe[:50]
print(hqm_dataframe)


# user enter how much to be spent in portfolio
portfolio_size = portfolio_input()

# calculate shares to be purchased for each stock to evenly distribute portfolio size
position_size = portfolio_size / len(hqm_dataframe.index)
print(position_size)

for row in hqm_dataframe.index:
    hqm_dataframe.loc[row, 'Number of Shares to Buy'] = math.floor(position_size / hqm_dataframe.loc[row, 'Price'])


#write result into an excel sheet
writer = pd.ExcelWriter('quant_momentum_strategy_result.xlsx', engine='xlsxwriter')
hqm_dataframe.to_excel(writer, sheet_name='Quantitative Momentum Strategy', index = False)
writer._save()

