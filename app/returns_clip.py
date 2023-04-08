from pandas_datareader import data as pdr
from datetime import date
import yfinance as yf
yf.pdr_override()
import datetime
import pandas as pd
import numpy as np
import statsmodels.api as sm
import pywhatkit
import requests
import datetime
import pyautogui
import math

# data_inicio = '2023-03-20'
# data_fim = '2023-03-28'
# index = '^BVSP'


API_Key = 'bugli4v48v6vml4hnn10'
Stocks = ['SPY', 'QQQ', 'BNO', 'EWZ']

dict_stock_data ={}
now = datetime.datetime.now()

msg = 'returns @ ' + str(now.hour) + ':' + str(now.minute) + '\n\n'

for element in Stocks:
    response = requests.get('https://finnhub.io/api/v1/quote?symbol='           + element + '&token=' + API_Key)
    print('https://finnhub.io/api/v1/quote?symbol=' + element + '&token=' + API_Key)
    dict_stock_data[element] = response.json()
    dict_stock_data[element]['Hora'] = datetime.datetime.now()
    dict_stock_data[element]['return'] = dict_stock_data[element]['c'] / dict_stock_data[element]['pc'] - 1
    msg += element + ' : ' + str(round(dict_stock_data[element]['return'] * 100, 2)) + '%\n'

pywhatkit.sendwhatmsg_to_group_instantly("LhTsd9SIr3y7PEc7WddPMy", msg, tab_close=True)

# today = date.today()
# start_date= datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
# end_date= datetime.datetime.strptime(data_fim, '%Y-%m-%d')
# print(today)
# data_index = pdr.get_data_yahoo(index, start=start_date, end=today)

# print(data_index)

