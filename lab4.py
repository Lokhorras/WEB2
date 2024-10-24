from flask import Blueprint, url_for, redirect, render_template, request, session
lab4 = Blueprint('lab4', __name__)

@lab4.route('/lab4/')
def lab3_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "/lab4/div-form", "text": "Деление"},
        {"url": "/lab4/sum-form", "text": "Cумма"},
        {"url": "/lab4/sub-form", "text": "Вычитание"},
        {"url": "/lab4/mul-form", "text": "Умножение"},
        {"url": "/lab4/pow-form", "text": "Cтепень"},
        {"url": "/lab4/tree", "text": "Дерево"},
        {"url": "/lab4/login", "text": "Логин"},
    ]
    return render_template('/lab4/lab4.html', links=links, name=name, name_color=name_color, age=age)


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('/lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('/lab4/div.html', error='Анлаки нолик')
    result = x1 / x2
    return render_template('/lab4/div.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sum-form')
def sum_form():
    return render_template('/lab4/sum-form.html')

@lab4.route('/lab4/sum', methods=['POST'])
def sum():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    if x2 == '':
        x2 = 0
    x1 = int(x1)
    x2 = int(x2)
    result = x1 + x2
    return render_template('/lab4/sum.html', x1=x1, x2=x2, result=result)




@lab4.route('/lab4/mul-form')
def mul_form():
    return render_template('/lab4/mul-form.html')

@lab4.route('/lab4/mul', methods=['POST'])
def mul():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    if x2 == '':
        x2 = 1
    x1 = int(x1)
    x2 = int(x2)
    result = x1 * x2
    return render_template('/lab4/mul.html', x1=x1, x2=x2, result=result)


@lab4.route('/lab4/sub-form')
def sub_form():
    return render_template('/lab4/sub-form.html')

@lab4.route('/lab4/sub', methods=['POST'])
def sub():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    
    if x1 == '' or x2 == '':
        return render_template('/lab4/sub.html', error='Оба поля должны быть заполнены!')
    
    x1 = int(x1)
    x2 = int(x2)
    
    result = x1 - x2
    return render_template('/lab4/sub.html', x1=x1, x2=x2, result=result)




@lab4.route('/lab4/pow-form')
def pow_form():
    return render_template('/lab4/pow-form.html')

@lab4.route('/lab4/pow', methods=['POST'])
def pow():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('/lab4/pow.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('/lab4/pow.html', error='Нельзя возводить 0 в степень 0!')
    result = x1 ** x2
    return render_template('/lab4/pow.html', x1=x1, x2=x2, result=result)



tree_count = 0

@lab4.route('/lab4/tree', methods=['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)
    
    operation = request.form.get('operation')
    
    if operation == 'cut':
        if tree_count > 0:
            tree_count -= 1
    elif operation == 'plant':
        tree_count += 1
    else:
        return "Операция не выбрана", 400
        
    return redirect(url_for('lab4.tree'))


users = [
    {'login': 'Alex', 'password': '123', 'name': 'Александр', 'gender': 'male'},
    {'login': 'Bob', 'password': '555', 'name': 'Боб', 'gender': 'male'},
    {'login': '9mice', 'password': '777', 'name': 'Мышь', 'gender': 'female'},
    {'login': 'kaiangel', 'password': '888', 'name': 'Катя', 'gender': 'female'}
]

@lab4.route('/lab4/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        authorized = 'login' in session
        login = session.get('login', '')
        return render_template('/lab4/login.html', authorized=authorized, login=login)
    
    login = request.form.get('login')
    password = request.form.get('password')

    if not login:
        error = 'не введён логин'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    if not password:
        error = 'не введён пароль'
        return render_template('/lab4/login.html', error=error, authorized=False, login=login)

    for user in users:
        if login == user['login'] and password == user['password']:
            session['login'] = login
            session['name'] = user['name']
            return redirect('/lab4/welcome')
    
    error = 'неверные логин и/или пароль'
    return render_template('/lab4/login.html', error=error, authorized=False, login=login)

@lab4.route('/lab4/welcome')
def welcome():
    if 'login' not in session:
        return redirect('/lab4/login')
    
    name = session['name']
    return render_template('/lab4/welcome.html', name=name)

@lab4.route('/lab4/logout', methods=['POST'])
def logout():
    session.pop('login', None)
    session.pop('name', None)
    return redirect('/lab4/login')