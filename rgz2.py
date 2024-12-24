from flask import Flask, Blueprint, url_for, redirect, render_template, request, session, jsonify
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__)
rgz2.secret_key = '123'  
# Функция для подключения к базе данных
def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

# Функция для закрытия соединения с базой данных
def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Маршрут для отображения главной страницы
@rgz2.route('/rgz2/')
def labbss():
    return render_template('base.html', login=session.get('login'))

@rgz2.route('/rgz2/rest-api/login', methods=['POST'])
def api_loginn():
    if request.method == 'POST':
        # Проверяем тип запроса
        if not request.is_json:
            return jsonify({'success': False, 'error': 'Unsupported Media Type. JSON expected'}), 415

        data = request.get_json()  # Получаем данные
        login = data.get('login')
        password = data.get('password')

        if not login or not password:
            return jsonify({'success': False, 'error': 'Login and password are required'}), 400

        conn, cur = db_connect()
        cur.execute("SELECT login, role FROM users_new3 WHERE login=? AND password=?;", (login, password))
        user = cur.fetchone()
        db_close(conn, cur)

        if user:
            session['login'] = login
            session['role'] = user['role']
            return jsonify({'success': True, 'role': user['role']})
        else:
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

    elif request.method == 'GET':
        # Возвращаем страницу входа
        return render_template('rgz2/login.html')


# API для выхода
@rgz2.route('/rgz2/rest-api/logout', methods=['POST'])
def api_logoutt():
    session.pop('login', None)
    session.pop('role', None)
    return jsonify({'success': True})

# API для получения данных пользователя
@rgz2.route('/rgz2/rest-api/user', methods=['GET'])
def api_userr():
    if 'login' in session:
        conn, cur = db_connect()
        cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
        user = cur.fetchone()
        db_close(conn, cur)
        if user:
            return jsonify(dict(user))
        else:
            return jsonify({'error': 'User not found'}), 404
    else:
        return jsonify({'error': 'Not logged in'}), 401

# API для получения истории транзакций
@rgz2.route('/rgz2/rest-api/transfers', methods=['GET'])
def api_transfersr():
    if 'login' in session:
        user_login = session['login']
        conn, cur = db_connect()
        cur.execute(
            """
            SELECT sender_login, receiver_login, amount, timestamp 
            FROM transactions3
            WHERE sender_login = ? OR receiver_login = ?
            ORDER BY timestamp DESC;
            """,
            (user_login, user_login)
        )
        transactions = cur.fetchall()
        db_close(conn, cur)
        return jsonify([dict(txn) for txn in transactions])
    else:
        return jsonify({'error': 'Not logged in'}), 401

# API для перевода денег
@rgz2.route('/rgz2/rest-api/transfer', methods=['POST'])
def api_transferr():
    if 'login' in session:
        sender_login = session['login']
        receiver_account_number = request.json.get('receiver_account_number')
        amount = request.json.get('amount')
        if not receiver_account_number or not amount:
            return jsonify({'error': 'Missing fields'}), 400
        conn, cur = db_connect()
        try:
            cur.execute("SELECT balance FROM users_new3 WHERE login=?;", (sender_login,))
            sender_balance = cur.fetchone()['balance']
            if sender_balance < float(amount):
                return jsonify({'error': 'Insufficient funds'}), 400
            cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;", (receiver_account_number,))
            receiver = cur.fetchone()
            if not receiver:
                return jsonify({'error': 'Receiver not found'}), 404
            receiver_login = receiver['login']
            receiver_balance = receiver['balance']
            new_sender_balance = sender_balance - float(amount)
            new_receiver_balance = receiver_balance + float(amount)
            cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (new_sender_balance, sender_login))
            cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))
            cur.execute("INSERT INTO transactions3 (sender_login, receiver_login, amount) VALUES (?, ?, ?);", (sender_login, receiver_login, amount))
            conn.commit()
            db_close(conn, cur)
            return jsonify({'success': True})
        except Exception as e:
            conn.rollback()
            db_close(conn, cur)
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Not logged in'}), 401