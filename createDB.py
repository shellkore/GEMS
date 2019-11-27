import sqlite3

conn = sqlite3.connect('database.db')
print ("Opened database successfully")

conn.execute('CREATE TABLE host (name TEXT, email TEXT, phone INTEGER NOT NULL PRIMARY KEY,address TEXT)')
print ("Table host created successfully")

conn.execute('CREATE TABLE visitor (name TEXT, email TEXT, phone INTEGER NOT NULL PRIMARY KEY, host TEXT, checkin TEXT, checkout TEXT)')
print("table visitor created successfully")
conn.close()