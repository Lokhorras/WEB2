from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab3_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    links = [
        {"url": "/lab3/cookie", "text": "Куки"},
        {"url": "/lab3/del_cookie", "text": "delete_cookies"},
        {"url": "/lab3/form1", "text": "form1"},
        {"url": "/lab3/order", "text": "Бар"},
    ]
    return render_template('/lab3/lab3.html', links=links, name=name, name_color=name_color)

@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', '9mice', max_age=5)
    resp.set_cookie('age', '24')
    resp.set_cookie('name_color', 'magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name')
    resp.set_cookie('age')
    resp.set_cookie('name_color')
    return resp

@lab3.route('/lab3/form1')
def form1():
    errors = {}
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    sex = request.args.get('sex')
    return render_template('/lab3/form1.html', user=user, age=age, sex=sex, errors= errors)



@lab3.route('/lab3/order')
def order():
    return render_template('/lab3/order.html')
price = 0
@lab3.route('/lab3/pay')
def pay():
    global price
    drink=request.args.get('drink')
    #кофе 120р черный чай 80р зеленый 70
    if drink == 'cofee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70
    #добавка молока удорожает напиток на 30р а сахара на 10
    
    if request.args.get('milk') == 'on':
        price+=30
    if request.args.get('sugar') == 'on':
        price += 10
    return render_template('/lab3/pay.html', price=price)

@lab3.route('/lab3/success')
def success():
    global price
    return render_template('/lab3/success.html', price=price)