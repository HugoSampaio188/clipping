from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from datetime import timedelta
import calendar
import pywhatkit
import time

lista_de_paises = ['BR', 'US']#, 'GB', 'EA', 'DE', 'CH']

url_tradingeconomics = 'https://tradingeconomics.com/calendar'
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(url_tradingeconomics)
assert "Economic Calendar" in driver.title

table_id = driver.find_element(By.ID, 'calendar')
rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table

structured_releases = []


del rows[0]
del rows[0]

rows = rows[0::2]

if len(str((datetime.now() + timedelta(days=1)).day)) == 1:
    data_aux_day = '0' + str((datetime.now() + timedelta(days=1)).day)
else:
    data_aux_day = str((datetime.now() + timedelta(days=1)).day)

if str((datetime.now() + timedelta(days=1)).month) != str((datetime.now()).month):          
    data_aux_month = calendar.month_name[(datetime.now() + timedelta(days=1)).month]
else:
    data_aux_month = calendar.month_name[datetime.now().month]

if str((datetime.now() + timedelta(days=1)).year) != str((datetime.now()).year):
    data_aux_year = str((datetime.now() + timedelta(days=1)).year)
else:
    data_aux_year = str(datetime.now().year)

date_tomorrow = data_aux_month + ' ' + data_aux_day + ' ' + data_aux_year

for row in rows:
    if date_tomorrow in row.text:
        print('proxima data aqui')
        break           
    linha = row.find_elements(By.TAG_NAME, "td")
    dict_release = {}
    print(linha[1].text)
    if linha[1].text in lista_de_paises:
        print('\n\ndado US ou BR\n\n')
        dict_release['ReleaseHr'] = linha[0].text
        dict_release['Country'] = linha[1].text
        dict_release['ReleaseName'] = linha[4].text
        dict_release['Previous'] = linha[6].text
        dict_release['Consensus'] = linha[7].text
        structured_releases.append(dict_release)

if len(structured_releases) != 0:
    msg = 'Releases de hoje ' + str(datetime.now().day) + ' ' + calendar.month_name[datetime.now().month] + '\n\n'
    for data_release in structured_releases:        
        if len(str(data_release['Consensus'])) != 0:
            consensus_aux = ' - consensus: ' + data_release['Consensus']
        else:
            consensus_aux = ''
        if len(str(data_release['Consensus'])) != 0:
            previous_aux = ' - previous: ' + data_release['Previous']
        else:
            previous_aux = ''
        msg += data_release['ReleaseHr'] + ' ' + data_release['Country'] + ' ' + data_release['ReleaseName'].replace('/', '') + consensus_aux + previous_aux + '\n'
else:
    print('sem releases')
    exit()          

tabela = pd.DataFrame.from_dict(structured_releases)

print(tabela)
print(msg)

driver.close()

pywhatkit.sendwhatmsg_to_group_instantly("CLnTxvpomvD13yW7PvNHbZ", msg, tab_close=True)