import sqlite3

con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()

for row in cursor.execute('SELECT * FROM stuff'):
    print(row)

con.commit()
con.close()