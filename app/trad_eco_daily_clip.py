from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
from datetime import datetime
from datetime import timedelta
import calendar
import pywhatkit
import time

if datetime.today().weekday() in [5,6]:
    print('hoje eh fds, sem clip')
    time.sleep(15)
    exit()
elif datetime.now().hour < 9 or datetime.now().hour > 18:
    print('mkt fechado')
    time.sleep(15)
    exit()

lista_de_paises = ['BR', 'US']#, 'GB', 'EA', 'DE', 'CH']

url_tradingeconomics = 'https://tradingeconomics.com/calendar'
driver = webdriver.Chrome()
driver.implicitly_wait(5)
driver.get(url_tradingeconomics)
assert "Economic Calendar" in driver.title

table_id = driver.find_element(By.ID, 'calendar')
rows = table_id.find_elements(By.TAG_NAME, "tr") # get all of the rows in the table

structured_releases = []
structured_clip = []

# escrever deletion dos itens que estao depois do dia de amanha na lista

del rows[0]
del rows[0]

rows = rows[0::2]

print(type(calendar.month_name[datetime.now().month]))
print(type(str((datetime.now() + timedelta(days=1)).day)))

print(type(str(datetime.now().year)))



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

# date_tomorrow = 'April 14 2023'

for row in rows:
    if date_tomorrow in row.text:
        print('proxima data aqui')
        break
    # print('esse eh o row' + str(i) + '\n')
    # print(row.text)
    # i = i + 1
    linha = row.find_elements(By.TAG_NAME, "td")
    dict_release = {}
    print(linha[1].text)
    if linha[1].text in lista_de_paises:
        print('\n\ndado US ou BR\n\n')
        dict_release['ReleaseHr'] = linha[0].text
        dict_release['Country'] = linha[1].text
        dict_release['ReleaseName'] = linha[4].text
        dict_release['Actual'] = linha[5].text
        dict_release['Previous'] = linha[6].text
        dict_release['Consensus'] = linha[7].text
        dict_release['Forecast'] = linha[8].text
        structured_releases.append(dict_release)

        hora_release = int(dict_release['ReleaseHr'][0:2]) + 12 if dict_release['ReleaseHr'].split(" ")[1] == 'PM' else int(dict_release['ReleaseHr'][0:2])
        minuto_release = dict_release['ReleaseHr'].split(" ")[0][3:5]
        hora_release = 12 if hora_release == 24 else hora_release
        hora_release = 00 if hora_release == 12 else hora_release
        horario_release = str(hora_release) + ':' + str(minuto_release)
        horario_release_f = datetime.strptime(horario_release, '%H:%M')

        # hour_now = datetime.now().hour
        # min_now = datetime.now().minute

        hour_now = 9
        min_now = 5

        horario_end_range = horario_release_f.replace(hour=hour_now, minute=min_now, second=0)
        horario_start_range = horario_end_range - timedelta(minutes=12)

        print(horario_release_f)
        print(horario_end_range)
        print(horario_start_range)
        

        # if datetime.now().hour == hora_release:
        if horario_start_range < horario_release_f < horario_end_range:
            structured_clip.append(dict_release)

if len(structured_clip) != 0:
    msg = 'Releases last 10 min | Time: ' + str(hour_now) + ':' + str(min_now) + '\n\n'
    for data_release in structured_clip:
        msg += 'ReleaseHr: ' + data_release['ReleaseHr'] + '\n'
        msg += 'Country: ' + data_release['Country'] + '\n'
        msg += 'Data: ' + data_release['ReleaseName'].replace('/', '            ') + '\n'
        msg += 'Actual: ' + data_release['Actual'] + '\n'
        msg += 'Previous: ' + data_release['Previous'] + '\n'
        msg += 'Consensus: ' + data_release['Consensus'] + '\n'

        print('aqui')
        print(len(data_release['Consensus']))
        print(type(data_release['Consensus']))
        
        if len(data_release['Consensus']) == 0:
            situ = 'NA consenso'
        elif data_release['Actual'] > data_release['Consensus']:
            situ = 'Acima do consenso'
        elif data_release['Actual'] < data_release['Consensus']:
            situ = 'Abaixo do consenso'         
        elif data_release['Actual'] == data_release['Consensus']:
            situ = 'Em linha com consenso'
        else:
            situ = 'NA consenso'

        if data_release['Actual'] > data_release['Previous']:
            situ += ', sobe na margem'
        elif data_release['Actual'] < data_release['Previous']:         
            situ += ', desce na margem'

        msg += 'Review: ' + situ + '\n\n'
else:
    print('sem releases')
    exit()

tabela = pd.DataFrame.from_dict(structured_releases)

print(tabela)
print(msg)

driver.close()

pywhatkit.sendwhatmsg_to_group_instantly("LhTsd9SIr3y7PEc7WddPMy", msg, tab_close=True)

exit()

# print('testando')
# print(len(linha))
# print(linha[0].text) # + ' k ' + category.text + ' k' + actual.text + ' k' )

# for i, col in enumerate(rows):
#     col = driver.find_element(By.TAG_NAME, 'td').text
#     print(f'Row: {i}, Name: {col}')

# print(country.text  + ' ' + category.text + ' ' + actual.text + ' ' + previous.text + ' ' + consensus.text + ' ' + forecast.text + '\n') #prints text from the element

# print(Category[2])
# print(Category[2].text)

i = 0
while i < 4:
    Country = driver.find_elements(By.XPATH, '//tr[' + str(i) +']/td[2]')
    # Category = driver.find_elements(By.CLASS_NAME, 'calendar-event')
    Actual = driver.find_elements(By.XPATH, '//tr[' + str(i) +']/td[4]')
    Previous = driver.find_elements(By.XPATH, '//tr[' + str(i) +']/td[5]')
    Consensus = driver.find_elements(By.XPATH, '//tr[' + str(i) +']/td[6]')
    Forecast = driver.find_elements(By.XPATH, '//tr[' + str(i) +']/td[7]')
    # print(Country[0])
    print(Actual[0])
    print(Previous[0])
    print(Consensus[0])
    print(Forecast[0])

    # print(Country.text  + ' ' + Actual.text + ' ' + Previous.text + ' ' + Consensus.text + ' ' + Forecast.text + '\n')
    # + ' ' + Category[i].text
    i = i +1

# block_data_hoje_pais = "/html/body[@class='vsc-initialized']/form[@id='aspnetForm']/div[@class='container']/div[@class='row']/div[@class='col-lg-10']/div[@class='table-responsive panel panel-default']/table[@id='calendar']/tbody[1]/tr[1]/td[@class='calendar-item']/table/tbody/tr/td[@class='calendar-iso']"
# block_data_hoje_release = "/html/body[@class='vsc-initialized']/form[@id='aspnetForm']/div[@class='container']/div[@class='row']/div[@class='col-lg-10']/div[@class='table-responsive panel panel-default']/table[@id='calendar']/tbody[1]/tr[1]/td[3]"
# elem2 = driver.find_element(By.XPATH, block_data_hoje_release)
# elem = driver.find_element(By.CSS_SELECTOR, "a./brazil/igp-m-inflation-mom")
# /div[@class='conatiner']/div[@class='row'] 

# print(elem2.text)
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()



# driver = webdriver.Chrome()
# driver.get("http://www.python.org")
# assert "Python" in driver.title
# elem = driver.find_element(By.NAME, "q")
# elem.clear()
# elem.send_keys("pycon")
# elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
# driver.close()