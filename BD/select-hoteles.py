import sqlite3

conn = sqlite3.connect('test.bd')

user = "1"
cursor = conn.execute("SELECT * FROM HOTELES WHERE ID_HOTEL =?", [str(user)])


print "OK"
conn.close()
