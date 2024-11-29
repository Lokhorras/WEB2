from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def lab():
    return render_template('rgz/rgz.html', login=session.get('login'))

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'one',
            user = 'one',
            password = '123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()
# INSERT INTO users_new (id, full_name, login, password, phone, account_number, balance, role) 
# VALUES
# (1, 'John Doe', 'johndoe', '123', '+1234567890', '12345678', 1000.00, 'client'),
# (2, 'Jane Smith', 'janesmith', '123', '+0987654321', '09876543', 1500.00, 'client'),
# (3,'Alice Johnson', 'alicej', '123', '+1122334455', '11223344', 2000.00, 'manager'),
# (4,'Bob Brown', 'bobbrown', '123', '+6677889900', '66778899', 500.00, 'client'),
# (5,'Charlie Davis', 'charlied', '123', '+1231231234', '12312312', 3000.00, 'client'),
# (6,'Eva White', 'evawhite', '123', '+4564564567', '45645645', 2500.00, 'client'),
# (7,'Frank Green', 'frankg', '123', '+7897897890', '78978978', 1200.00, 'client'),
# (8,'Grace Lee', 'gracelee', '123', '+3213213210', '32132132', 1800.00, 'client'),
# (9,'Henry Clark', 'henryc', '123', '+9879879870', '98798798', 2200.00, 'manager'),
# (10,'Ivy Harris', 'ivyh', '123', '+6546546540', '65465465', 900.00, 'client');  
    
    
@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('rgz/login.html', error='Заполните поля')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT login, password FROM users_new WHERE login=%s;", (login, ))
    else:
        cur.execute("SELECT login, password FROM users_new WHERE login=?;", (login, ))   
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')

    # Проверка пароля в открытом виде
    if user['password'] != password:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')

    session['login'] = login
    session['password'] = password
    db_close(conn, cur)
    return render_template('rgz/success_login.html', login=login)


@rgz.route('/rgz/logout')
def logout():
    session.pop('login', None)
    session.pop('password', None)
    return redirect('rgz.lab')




@rgz.route('/rgz/transfer', methods=['GET', 'POST'])
def transfer():
    if 'login' not in session:
        return redirect('/rgz/login')

    if request.method == 'GET':
        return render_template('rgz/transfer.html')

    sender_login = session['login']
    receiver_account_number = request.form.get('receiver_account_number')
    amount = float(request.form.get('amount'))

    if not receiver_account_number or not amount:
        return render_template('rgz/transfer.html', error='Заполните все поля')

    conn, cur = db_connect()

    try:
        # Начало транзакции
        conn.autocommit = False

        # Получаем баланс отправителя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT balance FROM users_new WHERE login=%s;", (sender_login,))
        else:
            cur.execute("SELECT balance FROM users_new WHERE login=?;", (sender_login,))
        sender_balance = cur.fetchone()['balance']

        # Проверка достаточности средств
        if sender_balance < amount:
            return render_template('rgz/transfer.html', error='Недостаточно средств на счете')

        # Обновляем баланс отправителя
        new_sender_balance = sender_balance - amount
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users_new SET balance=%s WHERE login=%s;", (new_sender_balance, sender_login))
        else:
            cur.execute("UPDATE users_new SET balance=? WHERE login=?;", (new_sender_balance, sender_login))

        # Получаем логин и баланс получателя
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("SELECT login, balance FROM users_new WHERE account_number=%s;", (receiver_account_number,))
        else:
            cur.execute("SELECT login, balance FROM users_new WHERE account_number=?;", (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            return render_template('rgz/transfer.html', error='Получатель не найден')

        receiver_login = receiver['login']
        receiver_balance = receiver['balance']

        # Обновляем баланс получателя
        new_receiver_balance = receiver_balance + amount
        if current_app.config['DB_TYPE'] == 'postgres':
            cur.execute("UPDATE users_new SET balance=%s WHERE account_number=%s;", (new_receiver_balance, receiver_account_number))
        else:
            cur.execute("UPDATE users_new SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))

        cur.execute(
            """
            INSERT INTO transactions (sender_login, receiver_login, amount)
            VALUES (%s, %s, %s);
            """,
            (sender_login, receiver_login, amount)
        )

        # Фиксация транзакции
        conn.commit()
        db_close(conn, cur)

        return render_template(
            'rgz/transfer_success.html',
            amount=amount,
            receiver_login=receiver_login
        )

    except Exception as e:
        # Откат транзакции в случае ошибки
        conn.rollback()
        db_close(conn, cur)
        print(f"Error: {e}")  # Отладочное сообщение
        return render_template('rgz/transfer.html', error='Ошибка при переводе средств')


@rgz.route('/rgz/history')
def history():
    if 'login' not in session:
        return redirect('/rgz/login')
    
    user_login = session['login']
    conn, cur = db_connect()

    
    # Получаем историю переводов пользователя
    cur.execute(
        """
        SELECT sender_login, receiver_login, amount, timestamp 
        FROM transactions
        WHERE sender_login = %s OR receiver_login = %s
        ORDER BY timestamp DESC;
        """,
        (user_login, user_login)
    )
    transactions = cur.fetchall()
    conn.commit()

    return render_template('rgz/history.html', transactions=transactions)



@rgz.route('/rgz/account')
def account():
    if 'login' not in session:
        return redirect('/rgz/login')

    conn, cur = db_connect()

    if current_app.config['DB_TYPE'] == 'postgres':
        cur.execute("SELECT * FROM users_new WHERE login=%s;", (session['login'],))
    else:
        cur.execute("SELECT * FROM users_new WHERE login=?;", (session['login'],))

    user = cur.fetchone()
    db_close(conn, cur)

    return render_template('rgz/account.html', user=user)








