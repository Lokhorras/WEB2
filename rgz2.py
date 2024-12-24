from flask import Blueprint, jsonify, request, session, redirect, render_template
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__)

def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        return conn, cur
    except Exception as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise

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
        try:
            # Получаем данные из запроса
            username = request.json.get('username')  # 'login' в вашей таблице
            password = request.json.get('password')

            if not username or not password:
                return jsonify({'error': 'Логин и пароль обязательны'}), 400

            # Подключаемся к базе данных
            conn, cur = db_connect()
            try:
                # Выбираем пользователя по логину и паролю
                cur.execute("SELECT * FROM users_new3 WHERE login = ? AND password = ?", (username, password))
                user = cur.fetchone()

                if user:
                    # Сохраняем данные в сессии
                    session['user_id'] = user['id']
                    session['username'] = user['login']
                    session['role'] = user['role']
                    return jsonify({'message': 'Вход выполнен успешно', 'username': user['login']}), 200
                else:
                    return jsonify({'error': 'Неверный логин или пароль'}), 401
            finally:
                db_close(conn, cur)
        except Exception as e:
            # Логируем ошибку для отладки
            return jsonify({'error': str(e)}), 500

    # Возвращаем HTML-форму, если запрос GET
    return render_template('rgz2/login.html')