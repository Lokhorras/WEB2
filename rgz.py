from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
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

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login = request.form.get('login')
    password = request.form.get('password')

    if not (login or password):
        return render_template('rgz/login.html', error='Заполните поля')

    conn, cur = db_connect()

    cur.execute("SELECT login, password, role FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()

    if not user:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')

    if user['password'] != password:
        db_close(conn, cur)
        return render_template('rgz/login.html', error='Логин и/или пароль неверны')

    # Сохраняем данные пользователя в сессии
    session['login'] = login
    session['role'] = user['role']  # Сохраняем роль пользователя
    db_close(conn, cur)
    return render_template('rgz/success_login.html', login=login)



@rgz.route('/rgz/transfer', methods=['GET', 'POST'])
def transfer():
    if 'login' not in session:
        return redirect('/rgz/login')

    if request.method == 'GET':
        return render_template('rgz/transfer.html')

    sender_login = session['login']
    receiver_account_number = request.form.get('receiver_account_number')
    amount = int(request.form.get('amount'))

    if not receiver_account_number or not amount:
        return render_template('rgz/transfer.html', error='Заполните все поля')

    conn, cur = db_connect()

    try:
        # Начало транзакции
        conn.isolation_level = None  # Отключаем autocommit
        cur.execute("BEGIN;")

        # Получаем баланс отправителя
        cur.execute("SELECT balance FROM users_new3 WHERE login=?;", (sender_login,))
        sender_balance = cur.fetchone()['balance']

        # Проверка достаточности средств
        if sender_balance < amount:
            return render_template('rgz/transfer.html', error='Недостаточно средств на счете')

        # Обновляем баланс отправителя
        new_sender_balance = sender_balance - amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (new_sender_balance, sender_login))

        # Получаем логин и баланс получателя
        cur.execute("SELECT login, balance FROM users_new3 WHERE account_number=?;", (receiver_account_number,))
        receiver = cur.fetchone()

        if not receiver:
            return render_template('rgz/transfer.html', error='Получатель не найден')

        receiver_login = receiver['login']
        receiver_balance = receiver['balance']

        # Обновляем баланс получателя
        new_receiver_balance = receiver_balance + amount
        cur.execute("UPDATE users_new3 SET balance=? WHERE account_number=?;", (new_receiver_balance, receiver_account_number))

        cur.execute(
            """
            INSERT INTO transactions3 (sender_login, receiver_login, amount)
            VALUES (?, ?, ?);
            """,
            (sender_login, receiver_login, amount)
        )

        # Фиксация транзакции
        cur.execute("COMMIT;")
        db_close(conn, cur)

        return render_template(
            'rgz/transfer_success.html',
            amount=amount,
            receiver_login=receiver_login
        )

    except Exception as e:
        # Откат транзакции в случае ошибки
        cur.execute("ROLLBACK;")
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
        FROM transactions3
        WHERE sender_login = ? OR receiver_login = ?
        ORDER BY timestamp DESC;
        """,
        (user_login, user_login)
    )
    transactions3 = cur.fetchall()
    conn.close()  # Закрываем соединение с базой данных

    return render_template('rgz/history.html', transactions3=transactions3)


@rgz.route('/rgz/account')
def account():
    if 'login' not in session:
        return redirect('/rgz/login')

    conn, cur = db_connect()

    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (session['login'],))
    user = cur.fetchone()
    db_close(conn, cur)

    return render_template('rgz/account.html', user=user)

@rgz.route('/rgz/logout')
def logoutt():
    # Удаляем данные о пользователе из сессии
    session.pop('login', None)
    session.pop('password', None)
    # Перенаправляем на страницу входа
    return redirect('/rgz/login')

# Функция для проверки, является ли текущий пользователь менеджером
def is_manager():
    if 'login' not in session:
        return False
    conn, cur = db_connect()
    cur.execute("SELECT role FROM users_new3 WHERE login=?;", (session['login'],))
    user = cur.fetchone()
    db_close(conn, cur)
    return user and user['role'] == 'manager'

# Маршрут для создания нового пользователя
@rgz.route('/rgz/create_user', methods=['GET', 'POST'])
def create_user():
    if not is_manager():
        return redirect('/rgz/login')

    if request.method == 'GET':
        return render_template('rgz/create_user.html')

    # Обработка POST-запроса
    full_name = request.form.get('full_name')
    login = request.form.get('login')
    password = request.form.get('password')
    phone = request.form.get('phone')
    account_number = request.form.get('account_number')
    balance = float(request.form.get('balance', 0))  # По умолчанию баланс 0
    role = request.form.get('role', 'client')  # По умолчанию роль клиент

    if not full_name or not login or not password or not phone or not account_number:
        return render_template('rgz/create_user.html', error='Заполните все поля')

    hashed_password = generate_password_hash(password)

    conn, cur = db_connect()
    try:
        cur.execute(
            """
            INSERT INTO users_new3 (full_name, login, password, phone, account_number, balance, role)
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """,
            (full_name, login, hashed_password, phone, account_number, balance, role)
        )
        conn.commit()
        db_close(conn, cur)
        return redirect('/rgz/account')
    except Exception as e:
        db_close(conn, cur)
        return render_template('rgz/create_user.html', error=f'Ошибка при создании пользователя: {str(e)}')

# Маршрут для редактирования пользователя
@rgz.route('/rgz/edit_user/<login>', methods=['GET', 'POST'])
def edit_user(login):
    if not is_manager():
        return redirect('/rgz/login')

    conn, cur = db_connect()
    cur.execute("SELECT * FROM users_new3 WHERE login=?;", (login,))
    user = cur.fetchone()
    db_close(conn, cur)

    if not user:
        return render_template('rgz/edit_user.html', error='Пользователь не найден')

    if request.method == 'GET':
        return render_template('rgz/edit_user.html', user=user)

    # Обработка POST-запроса
    full_name = request.form.get('full_name')
    password = request.form.get('password')
    phone = request.form.get('phone')
    account_number = request.form.get('account_number')
    balance = float(request.form.get('balance', 0))
    role = request.form.get('role', 'client')

    conn, cur = db_connect()
    try:
        if full_name:
            cur.execute("UPDATE users_new3 SET full_name=? WHERE login=?;", (full_name, login))
        if password:
            hashed_password = generate_password_hash(password)
            cur.execute("UPDATE users_new3 SET password=? WHERE login=?;", (hashed_password, login))
        if phone:
            cur.execute("UPDATE users_new3 SET phone=? WHERE login=?;", (phone, login))
        if account_number:
            cur.execute("UPDATE users_new3 SET account_number=? WHERE login=?;", (account_number, login))
        if balance is not None:
            cur.execute("UPDATE users_new3 SET balance=? WHERE login=?;", (balance, login))
        if role:
            cur.execute("UPDATE users_new3 SET role=? WHERE login=?;", (role, login))

        conn.commit()
        db_close(conn, cur)
        return redirect('/rgz/account')
    except Exception as e:
        db_close(conn, cur)
        return render_template('rgz/edit_user.html', user=user, error=f'Ошибка при редактировании пользователя: {str(e)}')

# Маршрут для удаления пользователя
@rgz.route('/rgz/delete_user/<login>', methods=['POST'])
def delete_user(login):
    if not is_manager():
        return redirect('/rgz/login')

    conn, cur = db_connect()
    try:
        cur.execute("DELETE FROM users_new3 WHERE login=?;", (login,))
        conn.commit()
        db_close(conn, cur)
        return redirect('/rgz/account')
    except Exception as e:
        db_close(conn, cur)
        return render_template('rgz/account.html', error=f'Ошибка при удалении пользователя: {str(e)}')