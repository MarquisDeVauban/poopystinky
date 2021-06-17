import sqlite3

con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()

cursor.execute(f'CREATE TABLE stuff (Item_Url TEXT, Date TEXT, Median TEXT)')
con.commit()

print('Table Created')
con.close()
#serves just to create the table for the sql database - 16 Jun 21