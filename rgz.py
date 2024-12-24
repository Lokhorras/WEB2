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

@rgz.route('rgz/api/login', methods=['POST'])
def api_login():
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

@rgz.route('rgz/api/logout', methods=['POST'])
def api_logout():
    session.pop('login', None)
    session.pop('role', None)
    return jsonify({'message': 'Успешный выход'}), 200

@rgz.route('rgz/api/transfer', methods=['POST'])
def api_transfer():
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

@rgz.route('rgz/api/history', methods=['GET'])
def api_history():
    if 'login' not in session:
        return jsonify({'error': 'Необходима авторизация'}), 401

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
    transactions = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)

    return jsonify({'transactions': transactions}), 200

@rgz.route('rgz/api/account', methods=['GET'])
def api_account():
    if 'login' not in session:
        return jsonify({'error': 'Необходима авторизация'}), 401

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = dict(cur.fetchone())
    db_close(conn, cur)

    return jsonify({'user': user}), 200

@rgz.route('rgz/api/create_user', methods=['POST'])
def api_create_user():
    if session.get('role') != 'manager':
        return jsonify({'error': 'Недостаточно прав'}), 403

    data = request.get_json()
    required_fields = ['full_name', 'login', 'password', 'phone', 'account_number', 'balance', 'role']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Заполните все поля'}), 400

    conn, cur = db_connect()
    try:
        cur.execute(
            """
            INSERT INTO users_new3 (full_name, login, password, phone, account_number, balance, role)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (data['full_name'], data['login'], data['password'], data['phone'],
            data['account_number'], data['balance'], data['role'])
        )
        conn.commit()
        db_close(conn, cur)
        return jsonify({'message': 'Пользователь успешно создан'}), 201
    except Exception as e:
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@rgz.route('rgz/api/edit_user/<login>', methods=['PUT'])
def api_edit_user(login):
    if session.get('role') != 'manager':
        return jsonify({'error': 'Недостаточно прав'}), 403

    data = request.get_json()
    conn, cur = db_connect()

    try:
        fields_to_update = []
        values = []
        for field, value in data.items():
            fields_to_update.append(f"{field} = ?")
            values.append(value)

        values.append(login)
        cur.execute(f"UPDATE users_new3 SET {', '.join(fields_to_update)} WHERE login = ?;", values)

        conn.commit()
        db_close(conn, cur)
        return jsonify({'message': 'Пользователь успешно обновлен'}), 200
    except Exception as e:
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@rgz.route('rgz/api/delete_user/<login>', methods=['DELETE'])
def api_delete_user(login):
    if session.get('role') != 'manager':
        return jsonify({'error': 'Недостаточно прав'}), 403

    conn, cur = db_connect()
    try:
        cur.execute("DELETE FROM users_new3 WHERE login=?;", (login,))
        conn.commit()
        db_close(conn, cur)
        return jsonify({'message': 'Пользователь успешно удален'}), 200
    except Exception as e:
        db_close(conn, cur)
        return jsonify({'error': f'Ошибка: {str(e)}'}), 500

@rgz.route('rgz/api/manage_users', methods=['GET'])
def api_manage_users():
    if session.get('role') != 'manager':
        return jsonify({'error': 'Недостаточно прав'}), 403

    conn, cur = db_connect()
    cur.execute("SELECT login, full_name, role FROM users_new3;")
    users = [dict(row) for row in cur.fetchall()]
    db_close(conn, cur)

    return jsonify({'users': users}), 200
