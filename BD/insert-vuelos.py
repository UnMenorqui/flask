import sqlite3

conn = sqlite3.connect('test.bd')

conn.execute("INSERT INTO USERS (ID_VUELO, COMPANYIA, ORIGEN, DESTINO) \
	VALUES ('1', 'AIRLINES','BARCELONA', 'MADRID');");

conn.commit()
print "OK"
conn.close()
