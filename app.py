#!flask/bin/python
from flask import Flask, jsonify, send_file, request, make_response, render_template, flash, Response, stream_with_context
from flask_cors import CORS, cross_origin # habilitem cross domain api
from flask_httpauth import HTTPBasicAuth
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

import sqlite3, requests, os, hashlib, uuid, json, sys

auth = HTTPBasicAuth()

def new_salted_password(password):
    salt = uuid.uuid4().hex
    return str(hashlib.sha512(password + salt).hexdigest())

@auth.get_password
def get_password(username):
    conn = sqlite3.connect('users.bd')
    password = get_user_password(username, conn)
    conn.close()
    return password


def exist_user(user):
    conn = sqlite3.connect('users.bd')
    cursor = conn.execute("SELECT * FROM USUARIOS WHERE ID_USUARIO =?", [str(user)])
    if not cursor.fetchall():
        conn.close()
        return False
    else:
        conn.close()
        return True


def get_user_password(user, conn):
    cursor = conn.execute("SELECT password FROM USUARIOS WHERE ID_USUARIO =?", [str(user)])
    return cursor.fetchone()[0]


def sign_up_user(user, password):
    conn = sqlite3.connect('users.bd')
    password = hashlib.sha512(str(password).encode('utf-8')).hexdigest()
    conn.execute("INSERT INTO USUARIOS (ID_USUARIO, PASSWORD) VALUES (?, ?);", [str(user), password]);

    conn.commit()
    conn.close()


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

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
    print("OK")
    conn.close()
    return render_template('login.html')


@app.route('/api/<user>/<fileName>/tokenizer', methods=['GET'])
@auth.login_required
def get_token_from_link(user, fileName):
    if auth.username() == user:
        conn = sqlite3.connect('users.bd')
        conn.close()

        token = uuid.uuid4().hex
        while token in files_tokens:
            token = uuid.uuid4().hex
        
        files_tokens[token] = [user]
        return jsonify(success=True, token=token)
    else:
        return unauthorized()


@app.route('/api/signup', methods=["POST"])
def sign_up():
    # FALTA MIRAR QUE NO EXISTA EL USER (ficar try exception)
    user = request.get_json()
    r = requests.post(URL_API + '/uri?t=mkdir&name=' + user['user'])
    sign_up_user(user['user'], user['password'], r.text)
    return jsonify(success=True)


@app.route('/login', methods=["POST"])
def sign_in():
    if exist_user(request.form['name']):
        password = get_password(request.form['name'])
        if request.form['password'] == password:
            return jsonify(success=True)
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


if __name__ == '__main__':
    app.secret_key = 'apiopi'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
