from flask import Blueprint, jsonify, request, session, redirect
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__)

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

@rgz2.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    login = data.get('login')
    password = data.get('password')

    if not (login and password):
        return jsonify({"error": "Заполните поля"}), 400

    conn, cur = db_connect()

    cur.execute("SELECT login, password, role FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user or user['password'] != password:
        db_close(conn, cur)
        return jsonify({"error": "Логин и/или пароль неверны"}), 401

    session['login'] = login
    session['role'] = user['role']
    db_close(conn, cur)
    return jsonify({"message": "Успешный вход", "login": login, "role": user['role']}), 200

@rgz2.route('/api/transfer', methods=['POST'])
def api_transfer():
    if 'login' not in session:
        return jsonify({"error": "Необходимо войти в систему"}), 401

    data = request.get_json()
    receiver_account_number = data.get('receiver_account_number')
    amount = data.get('amount')

    if not receiver_account_number or not amount:
        return jsonify({"error": "Заполните все поля"}), 400

    conn, cur = db_connect()
    sender_login = session['login']

    try:
        conn.isolation_level = None
        cur.execute("BEGIN;")

        cur.execute("SELECT balance FROM users_new3 WHERE login=?;", (sender_login,))
        sender_balance = cur.fetchone()['balance']

        if sender_balance < amount:
            return jsonify({"error": "Недостаточно средств"}), 400

        new_sender_balance = sender_balance - amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (new_sender_balance, sender_login))

        cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;", (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            return jsonify({"error": "Получатель не найден"}), 404

        receiver_login = receiver['login']
        new_receiver_balance = receiver['balance'] + amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))

        cur.execute("INSERT INTO transactions3 (sender_login, receiver_login, amount) VALUES (?, ?, ?);",
                    (sender_login, receiver_login, amount))
        cur.execute("COMMIT;")
        db_close(conn, cur)
        return jsonify({"message": "Перевод выполнен", "amount": amount, "receiver_login": receiver_login}), 200

    except Exception as e:
        cur.execute("ROLLBACK;")
        db_close(conn, cur)
        return jsonify({"error": f"Ошибка при переводе: {str(e)}"}), 500

@rgz2.route('/api/history', methods=['GET'])
def api_history():
    if 'login' not in session:
        return jsonify({"error": "Необходимо войти в систему"}), 401

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
    return jsonify({"transactions": transactions3}), 200

@rgz2.route('/api/account', methods=['GET'])
def api_account():
    if 'login' not in session:
        return jsonify({"error": "Необходимо войти в систему"}), 401

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = dict(cur.fetchone())
    db_close(conn, cur)
    return jsonify({"account": user}), 200

@rgz2.route('/api/logout', methods=['POST'])
def api_logout():
    session.clear()
    return jsonify({"message": "Вы успешно вышли из системы"}), 200

@rgz2.route('/interface')
def rgz2_interface():
    return '''
    <!doctype html>
    <html>
        <head>
            <title>rgz2 Interface</title>
            <script src="/static/script.js" defer></script>
        </head>
        <body>
            <h1>rgz2 Interface</h1>
            <!-- Добавить сюда HTML-формы или скрипты для взаимодействия с API -->
        </body>
    </html>
    '''