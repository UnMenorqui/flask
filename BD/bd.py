import sqlite3

conn = sqlite3.connect('test.bd')

conn.execute('''CREATE TABLE IF NOT EXISTS USUARIOS
	(ID_USUARIO TEXT PRIMARY KEY NOT NULL,
	PASSWORD TEXT);''')

conn.execute('''CREATE TABLE IF NOT EXISTS VUELOS
	(ID_VUELO INTEGER PRIMARY KEY NOT NULL,
	COMPANYIA TEXT,
	ORIGEN TEXT,
	DESTINO TEXT);''')

conn.execute('''CREATE TABLE IF NOT EXISTS HOTELES
	(ID_HOTEL TEXT PRIMARY KEY NOT NULL,
	NOM_HOTEL TEXT,
	CADENA TEXT,
	CALLE TEXT,
	NUMERO INTEGER,
	CODIGO_POSTAL INTEGER,
	CIUDAD TEXT);''')
print ("OK")
conn.close()