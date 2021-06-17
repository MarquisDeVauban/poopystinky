import sqlite3

con = sqlite3.connect('itemDataBase.db')
cursor = con.cursor()

cursor.execute(f'CREATE TABLE stuff (Item_Url TEXT, Date TEXT, Median TEXT)')

#serves just to create the table for the sql database - 16 Jun 21