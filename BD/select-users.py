import sqlite3

conn = sqlite3.connect('test.bd')

user = "toni"
cursor = conn.execute("SELECT PASSWORD FROM USERS WHERE ID_USUARIO=?", [str(user)])

print "OK"
conn.close()
