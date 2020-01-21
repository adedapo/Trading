import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import plotly.io as pio
import plotly.graph_objs as go

my_share = share.Share('ACB')
symbol_data = None

try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_DAY,
                                          10,
                                          share.FREQUENCY_TYPE_MINUTE,
                                          5)

except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

timestamp = [datetime.utcfromtimestamp(i/1000) for i in symbol_data['timestamp']]
trace = go.Candlestick(x=timestamp, open=symbol_data['open'], high=symbol_data['high'], low=symbol_data['low'], close=symbol_data['close'])
data = [trace]
grp = go.Figure(data)
pio.write_html(grp, file='correlations.html', auto_open=True)