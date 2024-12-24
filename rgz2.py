from flask import Blueprint, jsonify, request, session, redirect, render_template
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

@rgz2.route('/rgz2/')
def mainn():
    return render_template('rgz2/index.html')

@rgz2.route('/rgz2/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Получение данных из запроса
        username = request.json.get('username')
        password = request.json.get('password')

        if not username or not password:
            return jsonify({'error': 'Логин и пароль обязательны'}), 400

        # Подключение к базе данных
        conn, cur = db_connect()
        try:
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()
            if user:
                # Сохраняем данные пользователя в сессии
                session['user_id'] = user['id']
                session['username'] = user['username']
                session['role'] = user['role']
                return jsonify({'message': 'Вход выполнен успешно', 'username': user['username']}), 200
            else:
                return jsonify({'error': 'Неверный логин или пароль'}), 401
        finally:
            db_close(conn, cur)

    # Если метод GET, возвращаем HTML-форму
    return render_template('rgz2/login.html')
