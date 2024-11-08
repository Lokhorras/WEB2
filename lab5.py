from flask import Blueprint, url_for, redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab5_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "1", "text": "/lab5/shablon"},
    ]
    return render_template('/lab5/lab5.html', links=links, name=name, name_color=name_color, age=age, login = session.get('login'))


def db_connect():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'one',
        user = 'one',
        password = '123'
    )
    cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
    
    

@lab5.route('/lab5/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn, cur = db_connect()

    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
        db_close(conn, cur)
        return render_template('lab5/register.html',
                                error = 'Такой уже есть')
    
    password_hash  =  generate_password_hash(password)
    cur.execute(f"INSERT INTO users (login, password) VALUES  ('{login}', '{password_hash}');")
    db_close(conn, cur)
    return render_template('lab5/success.html', login=login)
    
    
@lab5.route('/lab5/login', methods= ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab5/login.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/login.html', error = 'ЗАПОЛНИТЕ все поля')
    
    conn, cur = db_connect()
    cur = conn.cursor(cursor_factory = RealDictCursor)
    
    cur.execute(f"SELECT * FROM users WHERE login='{login}';")
    user = cur.fetchone()
    
    if not user:
        db_close(conn, cur)
        return render_template('lab5/login.html', error='Логин и/или пароль неверны')
    
    if not check_password_hash(user['password'], password):
        db_close(conn, cur)
        return render_template('lab5/login.html', error = 'Лог и/или пароль неверны')
    session['login'] = login
    cur.close()
    conn.close()
    return render_template('lab5/succes_login.html', login=login)


