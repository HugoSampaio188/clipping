import yfinance as yf
import pandas as pd
import os
import pywhatkit

data = pd.read_csv(os.getcwd() + '\\tickers.csv')
print(data)

# Replace 'AAPL' with the stock ticker you want to get the price for
# symbol = 'RRRP3.SA'

list_infos = []
lista_tirar = []
ticker_list = data['Ticker'].to_list()

for linha, element in enumerate(ticker_list):
    print(str(linha) + ' ' + element)
    response = yf.Ticker(element + '.SA')
    dict_infos = {}
    dict_infos['Ticker'] = element
    dict_infos['Previous Close'] = response.info['regularMarketPreviousClose']
    dict_infos['Last Price'] = response.info['regularMarketPrice']
    dict_infos['Return'] = dict_infos['Last Price']/dict_infos['Previous Close']-1
    list_infos.append(dict_infos)

list_infos_sorted = sorted(list_infos, key=lambda d: d['Return']) 

worst_returns = list_infos_sorted[0:5]
list_infos_sorted.reverse()
best_returns = list_infos_sorted[0:5]

print(worst_returns)
print(best_returns)

msg = 'Top 5 returns from today \n\n'
for element in best_returns:
    msg += element['Ticker'] + ' ' + str(round(element['Return']* 100, 2)) + '%\n'

msg += '\n\nWorst 5 returns from today \n\n'
for element in worst_returns:
    msg += element['Ticker'] + ' ' + str(round(element['Return']* 100, 2)) + '%\n'          

print(msg)

pywhatkit.sendwhatmsg_to_group_instantly("LhTsd9SIr3y7PEc7WddPMy", msg, tab_close=True)

# response = yf.Ticker(symbol)


# print(response.info['regularMarketPreviousClose'])
# print(response.info['regularMarketPrice'])
# print(response.info['regularMarketTime'])
# print(response.info['regularMarketChange'])


# # Construct the API URL
# url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}'

# # Make the request to the API
# response = requests.get(url)

# print(response)