import sqlite3

conn = sqlite3.connect('test.bd')

user = "1"
cursor = conn.execute("SELECT * FROM VUELOS WHERE ID_VUELO =?", [str(user)])

print "OK"
conn.close()
