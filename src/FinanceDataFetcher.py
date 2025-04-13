import yfinance as yf
import pandas as pd
import numpy as np

class FinancialData:
    def __init__(self,ticker,start='2020-01-01',end=None,interval='1d'):
        self.ticker = ticker
        self.interval = interval
        self.start = start
        self.end = end
        self.data = None

    def get_options_data(self):
        tk = yf.Ticker(self.ticker)
        # Expiration dates
        exps = tk.options

        # Get options for each expiration
        options = pd.DataFrame()
        for e in exps:
            opt = tk.option_chain(e)
            opt = pd.DataFrame()._append(opt.calls)._append(opt.puts)
            opt['expirationDate'] = e
            options = options._append(opt, ignore_index=True)

        # Bizarre error in yfinance that gives the wrong expiration date
        # Add 1 day to get the correct expiration date
        # Boolean column if the option is a CALL
        options['CALL'] = options['contractSymbol'].str[4:].apply(
            lambda x: "C" in x)

        options[['bid', 'ask', 'strike']] = options[['bid', 'ask', 'strike']].apply(pd.to_numeric)
        options['mark'] = (options['bid'] + options['ask']) / 2  # Calculate the midpoint of the bid-ask

        # Drop unnecessary and meaningless columns
        options = options.drop(
            columns=['contractSize', 'currency', 'change', 'percentChange', 'lastTradeDate', 'lastPrice'])
        print(options)

test = FinancialData('aapl')

test.get_options_data()