#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response, render_template, flash, Response, stream_with_context, session
from flask_cors import CORS, cross_origin # habilitem cross domain api
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

import sqlite3, requests, os, hashlib, uuid, json, sys

auth = HTTPBasicAuth()

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
