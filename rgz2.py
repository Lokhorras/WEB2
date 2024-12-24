from flask import Flask, render_template, request, session, jsonify, Blueprint
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__)


# Database connection helpers
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

# Routes
@rgz2.route('/rgz2/')
def indexxx():
    return render_template('index.html')

@rgz2.route('/rgz2/api/login', methods=['POST'])
def api_loginnn():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({'error': 'Заполните все поля'}), 400

    conn, cur = db_connect()
    cur.execute("SELECT login, password, role FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or user['password'] != password:
        db_close(conn, cur)
        return jsonify({'error': 'Логин и/или пароль неверны'}), 401

    session['login'] = login
    session['role'] = user['role']
    db_close(conn, cur)
    return jsonify({'message': 'Успешный вход', 'login': login, 'role': user['role']}), 200

@rgz2.route('/rgz2/api/logout', methods=['POST'])
def api_logout():
    session.pop('login', None)
    session.pop('role', None)
    return jsonify({'message': 'Успешный выход'}), 200

@rgz2.route('/rgz2/api/transfer', methods=['POST'])
def api_transferrr():
    if 'login' not in session:
        return jsonify({'error': 'Необходима авторизация'}), 401

    data = request.get_json()
    receiver_account_number = data.get('receiver_account_number')
    amount = data.get('amount')

    if not receiver_account_number or not amount:
        return jsonify({'error': 'Заполните все поля'}), 400

    sender_login = session['login']
    conn, cur = db_connect()

    try:
        conn.isolation_level = None
        cur.execute("BEGIN;")

        cur.execute("SELECT balance FROM users_new3 WHERE login=?;", (sender_login,))
        sender_balance = cur.fetchone()['balance']

        if sender_balance < amount:
            return jsonify({'error': 'Недостаточно средств'}), 400

        cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;",
                    (sender_balance - amount, sender_login))

        cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;",
                    (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            return jsonify({'error': 'Получатель не найден'}), 404

        cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;",
                    (receiver['balance'] + amount, receiver_account_number))

        cur.execute(
            """
            INSERT INTO transactions3 (sender_login, receiver_login, amount)
            VALUES (?, ?, ?);
            """,
            (sender_login, receiver['login'], amount))

        cur.execute("COMMIT;")
        db_close(conn, cur)

        return jsonify({'message': 'Перевод выполнен успешно', 'amount': amount, 'receiver': receiver['login']}), 200

    except Exception as e:
        cur.execute("ROLLBACK;")
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@rgz2.route('/rgz2/api/account', methods=['GET'])
def api_accounttt():
    if 'login' not in session:
        return jsonify({'error': 'Необходима авторизация'}), 401

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = dict(cur.fetchone())
    db_close(conn, cur)

    return jsonify({'user': user}), 200

