from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def lab():
    return render_template('rgz/rgz.html', login=session.get('login'))
# INSERT INTO users_new3 (id, full_name, login, password, phone, account_number, balance, role) 
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
def db_connect():
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

@rgz.route('rgz/api-rest/login', methods=['POST'])
def api_login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({'error': 'Заполните поля'}), 400

    conn, cur = db_connect()
    cur.execute("SELECT login, password, role FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user or user['password'] != password:
        return jsonify({'error': 'Логин и/или пароль неверны'}), 401

    session['login'] = login
    session['role'] = user['role']
    return jsonify({'message': 'Успешный вход', 'role': user['role']}), 200


@rgz.route('rgz/api-rest/transfer', methods=['POST'])
def api_transfer():
    if 'login' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 401

    data = request.json
    sender_login = session['login']
    receiver_account_number = data.get('receiver_account_number')
    amount = data.get('amount')

    if not receiver_account_number or not amount:
        return jsonify({'error': 'Заполните все поля'}), 400

    conn, cur = db_connect()
    try:
        conn.isolation_level = None
        cur.execute("BEGIN;")
        cur.execute("SELECT balance FROM users_new3 WHERE login=?;", (sender_login,))
        sender_balance = cur.fetchone()['balance']

        if sender_balance < amount:
            return jsonify({'error': 'Недостаточно средств на счете'}), 400

        new_sender_balance = sender_balance - amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (new_sender_balance, sender_login))
        cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;", (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            return jsonify({'error': 'Получатель не найден'}), 404

        new_receiver_balance = receiver['balance'] + amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))
        cur.execute("INSERT INTO transactions3 (sender_login, receiver_login, amount) VALUES (?, ?, ?);", (sender_login, receiver['login'], amount))
        cur.execute("COMMIT;")
        db_close(conn, cur)
        return jsonify({'message': 'Перевод выполнен успешно'}), 200

    except Exception as e:
        cur.execute("ROLLBACK;")
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка при переводе: {e}'}), 500


@rgz.route('rgz/api-rest/account', methods=['GET'])
def api_account():
    if 'login' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 401

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = cur.fetchone()
    db_close(conn, cur)
    return jsonify({'user': dict(user)}), 200


@rgz.route('rgz/api-rest/history', methods=['GET'])
def api_history():
    if 'login' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 401

    conn, cur = db_connect()
    cur.execute(
        "SELECT sender_login, receiver_login, amount, timestamp FROM transactions3 WHERE sender_login=? OR receiver_login=? ORDER BY timestamp DESC;",
        (session['login'], session['login'])
    )
    transactions = cur.fetchall()
    db_close(conn, cur)
    return jsonify({'transactions': [dict(tx) for tx in transactions]}), 200
