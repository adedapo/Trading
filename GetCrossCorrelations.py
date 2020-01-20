import pandas as pd
import matplotlib.pyplot as plot
import chart_studio
import chart_studio.plotly as py
import plotly.graph_objs as go
import plotly.io as pio
import numpy as np

from plotly.offline import download_plotlyjs, init_notebook_mode, iplot
# chart_studio.tools.set_credentials_file(username='alabiaa96', api_key='Ao41B0F8yGo00xzzxQqG')


data = pd.read_pickle('HistoricalMostPopular.pkl')
df = data.rolling(180).corr()
print(df.shape)

# corr_mtx = df.values
# text_info = np.round(corr_mtx, decimals=5).astype(str)
#
# x = 0
# for i in range(len(text_info)):
#     for j in range(len(text_info[0])):
#         if text_info[i,j]=='1.0':
#             text_info[i,j]=''     #edit the hover text to block out the self-correlations
#             corr_mtx[i,j]=np.nan  #convert correlations values of 1.0 to nan (doesnt show in heatmap)
#
# layout = go.Layout(
#     images=[dict(  # add custom image to top right corner of graph
#         source="main-logo-black.png",
#         xref="paper", yref="paper",
#         x=1.2, y=1.1,
#         sizex=0.32, sizey=0.32,
#         xanchor="right", yanchor="bottom")],
#
#     title=f'Return Correlation',
#
#     annotations=[
#         dict(x=-.1, y=-.13, xref='paper', yref='paper', showarrow=False,
#              text=f'*6-Month Rolling Correlation of Daily Returns; Source: {source} via CoinAPI', font=dict(size=10))
#     ],
#     # define size of graph
#     autosize=False,
#     width=600,
#     height=600,
#
#     # customzie ticks
#     xaxis=dict(ticklen=8, tickcolor='#fff'),
#     yaxis=dict(ticklen=8, tickcolor='#fff')
# )
#
# config = {
#     'showAxisDragHandles': False,  # prevent resize of axis
#     'toImageButtonOptions': {  # how users will save image
#         'format': 'png',  # one of png, svg, jpeg, webp
#         'filename': 'blockforcecapital_crypto_correlation',
#         'height': 600,  # size of saved image
#         'width': 600,
#         'scale': 1},  # Multiply title/legend/axis/canvas sizes by this factor
#
#     'showLink': False,
#
#     # prevent certain action buttons
#     'modeBarButtonsToRemove': ['sendDataToCloud', 'zoomIn2d', 'zoomOut2d', 'zoom2d', 'pan2d', 'select2d', \
#                                'lasso2d', 'autoScale2d', 'zoom3d', 'pan3d', 'orbitRotation', 'tableRotation',
#                                'hoverClosestCartesian', \
#                                'hoverCompareCartesian']}
#
# #create heatmap object with custom colorscale
# data=[go.Heatmap(z=corr_mtx, text=text_info, hoverinfo='text', colorscale=[[0.,'#ebcd86'],[1,'#37475b']])]
#
# #create plotly figure object
# fig = go.Figure(data=data, layout=layout)
#
# #plot figure inline
# plot(fig, config=config)

trace3 = go.Heatmap(z=df, x=df.columns, y=df.columns)
grp = go.Figure(trace3)
pio.write_html(grp, file='correlations.html', auto_open=True)
