from flask import Blueprint, request, jsonify, session
import sqlite3
from os import path

rgz = Blueprint('rgz', __name__)

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

@rgz.route('/rgz/rest-api/login', methods=['POST'])
def login():
    data = request.json
    login = data.get('login')
    password = data.get('password')

    if not login or not password:
        return jsonify({'error': 'Заполните поля'}), 400

    conn, cur = db_connect()
    cur.execute("SELECT login, password FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or user['password'] != password:
        db_close(conn, cur)
        return jsonify({'error': 'Логин и/или пароль неверны'}), 401

    session['login'] = login
    db_close(conn, cur)
    return jsonify({'message': 'Успешный вход', 'login': login})

@rgz.route('/rgz/rest-api/transfer', methods=['POST'])
def transfer():
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
            cur.execute("ROLLBACK;")
            return jsonify({'error': 'Недостаточно средств на счете'}), 400

        new_sender_balance = sender_balance - amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (new_sender_balance, sender_login))

        cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;", (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            cur.execute("ROLLBACK;")
            return jsonify({'error': 'Получатель не найден'}), 404

        receiver_login = receiver['login']
        receiver_balance = receiver['balance']

        new_receiver_balance = receiver_balance + amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))

        cur.execute(
            """
            INSERT INTO transactions3 (sender_login, receiver_login, amount)
            VALUES (?, ?, ?);
            """,
            (sender_login, receiver_login, amount)
        )

        cur.execute("COMMIT;")
        db_close(conn, cur)

        return jsonify({'message': 'Перевод выполнен успешно', 'amount': amount, 'receiver_login': receiver_login})

    except Exception as e:
        cur.execute("ROLLBACK;")
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка при переводе средств: {str(e)}'}), 500

@rgz.route('/rgz/rest-api/history', methods=['GET'])
def history():
    if 'login' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 401

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
    transactions3 = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)

    return jsonify({'transactions': transactions3})

@rgz.route('/rgz/rest-api/account', methods=['GET'])
def account():
    if 'login' not in session:
        return jsonify({'error': 'Требуется авторизация'}), 401

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = dict(cur.fetchone())
    db_close(conn, cur)

    return jsonify({'user': user})

@rgz.route('/rgz/rest-api/logout', methods=['POST'])
def api_logout():
    session.pop('login', None)
    return jsonify({'message': 'Вы успешно вышли из системы'})
