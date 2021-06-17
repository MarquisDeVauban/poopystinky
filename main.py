import requests
import statistics
import time
import sqlite3
import datetime

'''JWT Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJwQ2pjdE5tUDIwY1NQRUJMNGxqUmJyb1hiRlcwdnRWcyIsImNzcmZfdG9rZW4iOiIxYWIwOTM0ZjdjODQwN2YwYmQ0ZmRkMDEyY2RlYmRjOThlZGYyMTU4IiwiZXhwIjoxNjI4NzMwOTkwLCJpYXQiOjE2MjM1NDY5OTAsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImxvZ2luX3VhIjoiYidNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTEuMC40NDcyLjc3IFNhZmFyaS81MzcuMzYnIiwibG9naW5faXAiOiJiJzQ3LjIwNS42Ny4yMTYnIiwiand0X2lkZW50aXR5IjoiS0lSUUtwMWcxVU5PTGI0V1dhakQwUU1KNmN1aGFQOFAifQ.l4ExNAJDhbw2fRgCM8sTyxXku0TxuxTxJtG-zzjXVEk'''

thingy = requests.get('https://api.warframe.market/v1/items').json()
itemList = []
dt = datetime.datetime.today()
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
month = ''
dbDict = {}
con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()

for thingy0 in months:
    if dt.month == 1 + months.index(thingy0):
        month = months[months.index(thingy0)]

#loop assigns word months to numbers cuz i dont like numbers - 16 Jun 21

for item in thingy['payload']['items']:
    name = item['url_name']
    itemList.append(name)

#loop creates list of item urls into itemList - 14 Jun 21

for url in itemList:
    startTime = str(time.ctime())
    simpTimeStart = time.time()
    orderSetPrices = []

    ordersOf = requests.get(f'https://api.warframe.market/v1/items/{url}/orders').json()

    for order in ordersOf['payload']['orders']:
        gameStatus = order['user']['status']
        orderType = order['order_type']

        if gameStatus == 'ingame' and orderType == 'sell':
            orderSetPrices.append(order['platinum'])
    #loop checks if the order should be considered - 16 Jun 21

    if len(orderSetPrices) != 0:
        platMedianStr = str(statistics.median(orderSetPrices))
        dbDict[f'{url}'] = {'median': f'{platMedianStr}'}

    else:
        dbDict[f'{url}'] = {'median': 'null'}

    median = dbDict[f'{url}']['median']

    #if/else sets the median, has else case in case there are no offers since median must have an argument - 16 Jun 21

    cursor.execute(f'INSERT INTO stuff (Item_Url, Date, Median) VALUES ("{url}", "{dt.day} {month} {dt.year}", "{median}")')
    con.commit()

    #commits the data into the sql database - 16 Jun 21

    endTime = str(time.ctime())
    simpTimeEnd = time.time()

    simpTime = str(simpTimeEnd - simpTimeStart)
    print(f'COMPLETE {url} FROM {startTime} TO {endTime} | t = {simpTime}s | {orderSetPrices} | m = {median}')

    #just a little bit of relavent data pertaining to runtime of certain things - 14 Jun 21

#loop creates dictionary of all item urls and pairs them with dictionaries for median - need to add in averages and other stuff - 14 Jun 21
#function to add the data to the sql database has been added, forego averages for now - 16 Jun 21
print(dbDict)
con.close()
