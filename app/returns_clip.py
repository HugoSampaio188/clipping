from datetime import datetime
import pywhatkit
import requests
import time
import os

if datetime.now().weekday() in [5,6]:
    print('hoje eh fds, sem clip')
    time.sleep(15)
    exit()
elif datetime.now().hour < 9 or datetime.now().hour > 19:
    print('mkt fechado')
    time.sleep(15)
    exit()

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

# path = os.path.join("C:", os.sep, "Users", "hvshu", "OneDrive", "Área de Trabalho", "Estudos", "ProjetosGit", "clipping", "demofile.txt")
# f = open(path, "a")
# f.write("\nContent in file " + str(now) + "\n")
# f.write(msg)

# f.write('\nvai entrar na parte de mandar msg por wpp')

pywhatkit.sendwhatmsg_to_group_instantly("CLnTxvpomvD13yW7PvNHbZ", msg, tab_close=True, wait_time=40)

# f.write('\nchegou no final do script')

# f.close()

