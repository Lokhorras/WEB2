from flask import Blueprint, url_for, redirect, render_template, request, session
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
    return render_template('/lab5/lab5.html', links=links, name=name, name_color=name_color, age=age)


@lab5.route('/lab5/register', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab5/register.html')
    
    login = request.form.get('login')
    password = request.form.get('password')
    
    if not (login or password):
        return render_template('lab5/register.html', error='Заполните все поля!')
    
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'one',
        user = 'one',
        password = '123'
    )
    cur = conn.cursor()
    cur.execute(f"SELECT login FROM users WHERE login='{login}';")
    if cur.fetchone():
            cur.close()
            conn.close()
            return render_template('lab5/register.html',
                                error = 'Такой уже есть')
            
    cur.execute(f"INSERT INTO users (login, password) VALUES  ('{login}', '{password}');")
    conn.commit()
    cur.close()
    conn.close()
    return render_template('lab5/success.html', login=login)
    
    