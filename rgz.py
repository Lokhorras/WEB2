from flask import Blueprint, url_for, redirect, render_template, request, session, jsonify
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

@rgz.route('/rgz/')
def lab():
    return render_template('rgz/rgz.html', login=session.get('login'))

@rgz.route('/rgz/api/login', methods=['POST'])
def api_login():
    login = request.json.get('login')
    password = request.json.get('password')
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

@rgz.route('/rgz/api/logout', methods=['POST'])
def api_logout():
    session.pop('login', None)
    session.pop('role', None)
    return jsonify({'success': True})

@rgz.route('/rgz/api/user', methods=['GET'])
def api_user():
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

@rgz.route('/rgz/api/transfers', methods=['GET'])
def api_transfers():
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

@rgz.route('/rgz/api/transfer', methods=['POST'])
def api_transfer():
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