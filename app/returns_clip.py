from datetime import datetime
import pywhatkit
import requests
import time

'''if datetime.now().weekday() in [5,6]:
    print('hoje eh fds, sem clip')
    time.sleep(15)
    exit()
elif datetime.now().hour < 9 or datetime.now().hour > 19:
    print('mkt fechado')
    time.sleep(15)
    exit()'''

# data_inicio = '2023-03-20'
# data_fim = '2023-03-28'
# index = '^BVSP'


API_Key = 'bugli4v48v6vml4hnn10'
Stocks = ['SPY', 'QQQ', 'BNO', 'EWZ']

dict_stock_data ={}
now = datetime.now()

msg = 'returns @ ' + str(now.hour) + ':' + str(now.minute) + '\n\n'

for element in Stocks:
    response = requests.get('https://finnhub.io/api/v1/quote?symbol='           + element + '&token=' + API_Key)
    print('https://finnhub.io/api/v1/quote?symbol=' + element + '&token=' + API_Key)
    dict_stock_data[element] = response.json()
    dict_stock_data[element]['Hora'] = datetime.now()
    dict_stock_data[element]['return'] = dict_stock_data[element]['c'] / dict_stock_data[element]['pc'] - 1
    msg += element + ' : ' + str(round(dict_stock_data[element]['return'] * 100, 2)) + '%\n'

pywhatkit.sendwhatmsg_to_group_instantly("CLnTxvpomvD13yW7PvNHbZ", msg, tab_close=True, wait_time=40)

# today = date.today()
# start_date= datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
# end_date= datetime.datetime.strptime(data_fim, '%Y-%m-%d')
# print(today)
# data_index = pdr.get_data_yahoo(index, start=start_date, end=today)

# print(data_index)

