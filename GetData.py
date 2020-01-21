from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import pandas as pd

stock_list = pd.read_excel('MostPopular.xlsx')
stock_list = stock_list[stock_list.Symbol.notna()].Symbol
all_data = 0

for ticker in stock_list:
    my_share = share.Share(ticker)

    try:
        symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                              5,
                                              share.FREQUENCY_TYPE_DAY,
                                              1)

        tmark = [datetime.utcfromtimestamp(i / 1000) for i in symbol_data['timestamp']]
        try:
            assert(type(all_data) is pd.DataFrame)
        except:
            all_data = pd.DataFrame(index=tmark, columns=stock_list)
        all_data[ticker] = pd.Series(symbol_data['close'], index=tmark)

    except YahooFinanceError as e:
        print(e.message)
        try:
            all_data.drop(index=ticker)
        except:
            continue

all_data.to_pickle("HistoricalMostPopular.pkl")
