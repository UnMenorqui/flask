insert.pyimport sqlite3

conn = sqlite3.connect('test.bd')

conn.execute("INSERT INTO USERS (ID_USUARIO, PASSWORD) 	VALUES ('toni', 'toni');");

conn.commit()
print "OK"
conn.close()
