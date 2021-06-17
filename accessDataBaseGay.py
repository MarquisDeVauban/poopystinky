import sqlite3

con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()

command = ''

while True:
    command = input('pass: ')
    if command != 'end':
        for row in cursor.execute(command):
            print(row)
    else:
        break

con.commit()
con.close()
