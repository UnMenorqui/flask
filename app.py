#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response, render_template, flash, Response, stream_with_context, session
from flask_cors import CORS, cross_origin # habilitem cross domain api
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename
from flask_table import create_table, Table, Col

app = Flask(__name__)
CORS(app)

import sqlite3, requests, os, hashlib, uuid, json, sys

auth = HTTPBasicAuth()

class ItemTable(Table):
    number = Col('Number')
    company = Col('Company')
    origin = Col('Origin')
    destination = Col('Destination')



@auth.get_password
def get_password(username):
    conn = sqlite3.connect('users.bd')
    password = get_user_password(username, conn)
    conn.close()
    return password

def get_user_password(user, conn):
    cursor = conn.execute("SELECT password FROM USUARIOS WHERE ID_USUARIO =?", [str(user)])
    return cursor.fetchone()[0]

def exist_user(user):
    conn = sqlite3.connect('users.bd')
    cursor = conn.execute("SELECT * FROM USUARIOS WHERE ID_USUARIO =?", [str(user)])
    if not cursor.fetchall():
        conn.close()
        return False
    else:
        conn.close()
        return True


@app.route('/menu')
def menu():
    return render_template('menu.html')


@app.route('/')
def home():
    conn = sqlite3.connect('users.bd')
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
    conn.close()
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('menu.html')

@app.route('/login', methods=["POST"])
def sign_in():
    if exist_user(request.form['name']):
        password = get_password(request.form['name'])
        if request.form['password'] == password:
            session['logged_in'] = True
            return render_template('menu.html')
        else:
            return jsonify(success=False)
    return jsonify(success=False)



@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/do_register', methods=["POST"])
def do_register():
    if exist_user(request.form['name']):
        return jsonify(success=False)
    else:
        if (request.form['password']) == (request.form['password1']):
            conn = sqlite3.connect('users.bd')
            user = request.form['name']
            password = request.form['password']
            conn.execute("INSERT INTO USUARIOS (ID_USUARIO, PASSWORD) VALUES (?, ?);",[str(user),str(password)]);
            conn.commit()
            conn.close()
            return home()
        else:
            return jsonify(success=False)

@app.route('/altavuelo')
def altavuelo():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        return render_template('altavuelo.html')

@app.route('/do_altavuelo', methods=['POST'])
def do_altavuelo():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        vuelo_number = request.form['numero']
        vuelo_company = request.form['companyia']
        vuelo_origin = request.form['origen']
        vuelo_destination = request.form['destino']
        conn = sqlite3.connect('users.bd')
        conn.execute("INSERT INTO VUELOS (ID_VUELO, COMPANYIA, ORIGEN, DESTINO) VALUES (?, ?, ?, ?);",[str(vuelo_number),str(vuelo_company),str(vuelo_origin),str(vuelo_destination)]);
        conn.commit()
        conn.close()
        return menu()


@app.route('/buscarvuelo')
def buscarvuelo():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        return render_template('buscarvuelo.html')

@app.route('/do_buscarvuelo', methods=['POST'])
def do_buscarvuelo():
    vuelo_number = request.form['numero']
    vuelo_company = request.form['companyia']
    vuelo_origin = request.form['origen']
    vuelo_destination = request.form['destino']
    conn = sqlite3.connect('users.bd')
    if (vuelo_number == "") :
        if (vuelo_company == "") :
            if (vuelo_origin == "") :
                if (vuelo_destination == ""):
                     rs = conn.execute("SELECT * FROM vuelos")
                else:
                     rs = conn.execute("SELECT * from vuelos where destino=?",[str(vuelo_destination)])
            else :
                if (vuelo_destination == ""):
                     rs = conn.execute("SELECT * from vuelos where origen=?",[str(vuelo_origin)]);
                else:
                     rs = conn.execute("SELECT * from vuelos where destino=? and origen=?", [str(vuelo_destination),str(vuelo_origin)])
        else :
            if (vuelo_origin == "") :
                if (destino.equals("")):
                     rs = conn.execute("SELECT * from vuelos where companyia=?",[str(vuelo_origin)])
                else:
                     rs = conn.execute("SELECT * from vuelos where companyia=? and destino=?",[str(vuelo_company),str(vuelo_destination)])
            else :
                if (vuelo_destination == ""):
                     rs = conn.execute("SELECT * from vuelos where companyia=? and origen=?",[str(vuelo_company),str(vuelo_origin)])
                else:
                     rs = conn.execute("SELECT * from vuelos where companyia=? and destino=? and origen=?",[str(vuelo_company),str(vuelo_destination),str(vuelo_origin)])
    else :
        if (vuelo_company == ""):
            if (vuelo_origin == ""):
                if (vuelo_destination == ""):
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=?",[str(vuelo_number)])
                else:
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and destino=?",[str(vuelo_number),str(vuelo_destination)])
            else :
                if (vuelo_destination == ""):
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and origen=?",[str(vuelo_number), str(vuelo_origin)])
                else:
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and destino=? and origen=?", [str(vuelo_number),str(vuelo_destination),str(vuelo_origin)])
        else :
            if (vuelo_origin == "") :
                if (vuelo_destination == ""):
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and companyia=?", [str(vuelo_number), str(vuelo_company)])
                else:
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and companyia=? and destino=?",[str(vuelo_number),str(vuelo_company),str(vuelo_destination)])
            else :
                if (vuelo_destination == ""):
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and companyia=? and origen=?", [str(vuelo_number),str(vuelo_company),str(vuelo_origin)])
                else:
                    rs = conn.execute("SELECT * from vuelos where id_vuelo=? and companyia=? and destino=? and origen=?",[str(vuelo_number),str(vuelo_company),str(vuelo_destination),str(vuelo_origin)])

    return """
        <!DOCTYPE html>
        <html xmlns="http://www.w3.org/1999/xhtml">
        <head> 
            <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            <title>Menu</title>
            <link rel="stylesheet" type="text/css" href="/static/menu.css" />
            <link rel="stylesheet" tupe="text/css" href="/static/tabla.css" />
        </head>
        <body>
            <ul>
                <li><a href="menu">Home</a></li>
                <li class="dropdown">
                    <a href="#">Flights</a>
                    <div class="dropdown-content">
                        <a href="altavuelo">Register Flight</a>
                        <a href="buscarvuelo">Search Flight</a>
                    </div> 
                </li>
                
               <li class="dropdown">
                    <a href="#">Hotels</a>
                    <div class="dropdown-content">
                        <a href="altahotel">Register Hotel</a>
                        <a href="buscarhotel">Search Hotel</a>
                    </div> 
                </li>
                <li><a href="logout">Log Out</a></li>
            </ul>
            <div class="container">
                <div class="login-box">
                    <div class="box-header">
                        <h2>Searched Flights</h2>
                    </div>
                <table id="customers">
            <tr>
                <th><strong>Flight Number</strong></th>
                <th><strong>Company</strong></th>
                <th><strong>Origin</strong></th>
                <th><strong>Destination</strong></th>
            </tr>
                <tr>
                    <td>123</td>
                    <td>Airlines</td>
                    <td>Madrid</td>
                    <td>Barcelona</td>
                </tr>
                <tr>
                    <td>1235</td>
                    <td>Vueling</td>
                    <td>Granada</td>
                    <td>Menorca</td>
                </tr>
        
        </body>
    </html>"""
    conn.commit()
    conn.close()



@app.route('/altahotel')
def altahotel():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        return render_template('altahotel.html')

@app.route('/do_altahotel', methods=['POST'])
def do_altahotel():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        hotel_id = request.form['id_hotel']
        hotel_name = request.form['nombrehotel']
        hotel_chain = request.form['cadenahotelera']
        hotel_street = request.form['calle']
        hotel_number = request.form['numero']
        postal_code = request.form['codigopostal']
        hotel_city = request.form['ciudad']

        conn = sqlite3.connect('users.bd')
        conn.execute("INSERT INTO HOTELES (ID_HOTEL, NOM_HOTEL, CADENA, CALLE, NUMERO, CODIGO_POSTAL, CIUDAD) VALUES(?, ?, ?, ?, ?, ?, ?);",[str(hotel_id),str(hotel_name),str(hotel_chain),str(hotel_street),str(hotel_number),str(postal_code),str(hotel_city)]);
        conn.commit()
        conn.close()
        return menu()

@app.route('/buscarhotel')
def buscarhotel():
    if not session.get('logged_in'):
        return jsonify(success=False)
    else:
        return render_template('buscarhotel.html')

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

if __name__ == '__main__':
    app.secret_key = 'apiopi'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
