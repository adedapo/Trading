import sys
from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError
from datetime import datetime
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import pandas as pd
from numpy import isnan, nan

# stock_list = pd.read_excel('TopUnder25.xlsx')
# stock_list = stock_list[stock_list.Symbol.notna()].Symbol

probed = 'NOK'
chart_studio.tools.set_credentials_file(username='alabiaa96', api_key='Ao41B0F8yGo00xzzxQqG')

my_share = share.Share(probed)
symbol_data = None

try:
    symbol_data = my_share.get_historical(share.PERIOD_TYPE_YEAR,
                                          5,
                                          share.FREQUENCY_TYPE_DAY,
                                          1)

except YahooFinanceError as e:
    print(e.message)
    sys.exit(1)

timestamp = [datetime.utcfromtimestamp(i/1000) for i in symbol_data['timestamp']]
ma20 = pd.DataFrame(symbol_data['close']).rolling(window=1).mean()[0]
ma50 = pd.DataFrame(symbol_data['close']).rolling(window=20).mean()[0]

prev_sig = nan
# buy = [[], []]
# sell = [[], []]
owned = 0
pnl = [0]
pnl_time = []
profit = []
paid = 0
for i in range(len(ma20)):
    if isnan(ma50[i]):
        continue
    sig = ma20[i] > ma50[i]
    if isnan(prev_sig):
        prev_sig = sig
        continue
    if sig == prev_sig:
        continue
    if i+5>=len(ma20):
        break
    elif sig == 1:
        owned += 1
        paid = symbol_data['close'][i]
        pnl.append(pnl[-1] - symbol_data['close'][i])
        # pnl_time.append(timestamp[i])
        # buy[0].append(timestamp[i])
        # buy[1].append((symbol_data['close'][i+30]-symbol_data['close'][i])/symbol_data['close'][i])
    else:
        if owned > 0:
            pnl.append(pnl[-1] + symbol_data['close'][i])
            profit.append(symbol_data['close'][i] - paid)
            owned -= 1
            pnl_time.append(timestamp[i])
        # sell[0].append(timestamp[i])
        # sell[1].append((symbol_data['close'][i + 30] - symbol_data['close'][i]) / symbol_data['close'][i])
    prev_sig = sig

# print("Average gain after golden crosses:", sum(buy[1])/len(buy[1]))
# print("Average loss after death crosses:", sum(sell[1])/len(sell[1]))

trace0 = go.Scatter(x=timestamp, y=symbol_data['close'], name='Price')
# go.Candlestick(x=timestamp, open=symbol_data['open'], high=symbol_data['high'],
# low=symbol_data['low'], close=symbol_data['close'])
trace1 = go.Scatter(x=timestamp, y=ma20, name='20 HMA', line_color='green')
trace2 = go.Scatter(x=timestamp, y=ma50, name='50 HMA', line_color='red')
trace3 = go.Bar(x=pnl_time, y=profit, name='Profit')
data = [trace0, trace1, trace2, trace3]
py.plot(data)

print("Average profit is:", sum(profit)/len(profit), "\nAccuracy:", 100*sum([1 for i in range(len(profit)) if profit[i] > 0])/len(profit))

#
# trace1 = go.Scatter(x=buy[0], y=buy[1], name="Buy Gains")
# trace2 = go.Scatter(x=sell[0], y=sell[1], name="Sell Gains")
# data = [trace1, trace2]
# py.plot(data)
