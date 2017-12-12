import sqlite3

conn = sqlite3.connect('test.bd')

conn.execute("INSERT INTO USERS (ID_HOTEL,NOM_HOTEL, CADENA, CALLE, NUMERO, CODIGO_POSTAL, CIUDAD) \
	VALUES ('1', 'FIGOLS','NH-HOTELES','FIGOLS','15','08028','BARCELONA');");

conn.commit()
print "OK"
conn.close()
