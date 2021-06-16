import requests
import statistics
import time
import sqlite3

'''JWT Token: eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzaWQiOiJwQ2pjdE5tUDIwY1NQRUJMNGxqUmJyb1hiRlcwdnRWcyIsImNzcmZfdG9rZW4iOiIxYWIwOTM0ZjdjODQwN2YwYmQ0ZmRkMDEyY2RlYmRjOThlZGYyMTU4IiwiZXhwIjoxNjI4NzMwOTkwLCJpYXQiOjE2MjM1NDY5OTAsImlzcyI6Imp3dCIsImF1ZCI6Imp3dCIsImF1dGhfdHlwZSI6ImNvb2tpZSIsInNlY3VyZSI6ZmFsc2UsImxvZ2luX3VhIjoiYidNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvOTEuMC40NDcyLjc3IFNhZmFyaS81MzcuMzYnIiwibG9naW5faXAiOiJiJzQ3LjIwNS42Ny4yMTYnIiwiand0X2lkZW50aXR5IjoiS0lSUUtwMWcxVU5PTGI0V1dhakQwUU1KNmN1aGFQOFAifQ.l4ExNAJDhbw2fRgCM8sTyxXku0TxuxTxJtG-zzjXVEk'''

thingy = requests.get('https://api.warframe.market/v1/items').json()

itemList = []

for item in thingy['payload']['items']:
    name = item['url_name']
    itemList.append(name)

#loop creates list of item urls into itemList - 14 Jun 21

dbDict = {}

con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()
cursor.execute('CREATE TABLE stuff (itemurl text, date text, m1 text, m2 text, m3 text)')

for url in itemList:
    startTime = str(time.ctime())
    simpTimeStart = time.time()
    orderSetPrices = []

    ordersOf = requests.get('https://api.warframe.market/v1/items/%s/orders' % (url)).json()

    for order in ordersOf['payload']['orders']:
        #ask Mahlon/Hao why 'ordersOf' on its own then doing 'gameStatus = order['payload']['orders']' doenst work for accessing the keyvalues of the json
        gameStatus = order['user']['status']
        orderType = order['order_type']

        if gameStatus == 'ingame' and orderType == 'sell':
            orderSetPrices.append(order['platinum'])

    if len(orderSetPrices) != 0:
        platMedianStr = str(statistics.median(orderSetPrices))
        dbDict['%s' % (url)] = {'median': f'{platMedianStr}'}
    else:
        dbDict['%s' % (url)] = {'median': 'null'}

    median = dbDict['%s' % (url)]['median']

    cursor.execute(f'INSERT INTO stuff VALUES ({url}, {startTime}, {v })')
    endTime = str(time.ctime())
    simpTimeEnd = time.time()

    simpTime = str(simpTimeEnd - simpTimeStart)
    print('COMPLETE %s' % (url) + ' FROM %s' % (startTime) + ' TO %s' % (endTime) + ' | t = %s' % (simpTime) + ' s |', orderSetPrices, '| m = ', median)

#loop creates dictionary of all item urls and pairs them with dictionaries for median - need to add in averages and other stuff - 14 Jun 21
print(dbDict)
