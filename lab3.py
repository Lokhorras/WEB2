from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab3_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "/lab3/cookie", "text": "Куки"},
        {"url": "/lab3/del_cookie", "text": "delete_cookies"},
        {"url": "/lab3/form1", "text": "form1"},
        {"url": "/lab3/order", "text": "Бар"},
        {"url": "/lab3/settings", "text": "Настройки"},
        {"url": "/lab3/ticketform", "text": "Дорога"},
        {"url": "/lab3/settings/clear_cookies", "text": "Не люблю куки"},
        {"url": "/lab3/productss", "text": "Бренды"},
    ]
    return render_template('/lab3/lab3.html', links=links, name=name, name_color=name_color, age=age)

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
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'
    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'
    else:
        errors = ""
        return errors['']
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

@lab3.route('/lab3/settings/')
def settings():
    color = request.args.get('color')
    bgcolor = request.args.get('bgcolor')
    fsize = request.args.get('fsize')
    bordercolor = request.args.get('bordercolor')
    borderwidth = request.args.get('borderwidth')

    if color:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('color', color)
        return resp
    if bgcolor:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('bgcolor', bgcolor)
        return resp
    if fsize:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('fsize', fsize)
        return resp
    if bordercolor:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('bordercolor', bordercolor)
        return resp
    if borderwidth:
        resp = make_response(redirect('/lab3/settings/'))
        resp.set_cookie('borderwidth', borderwidth)
        return resp

    color = request.cookies.get('color')
    bgcolor = request.cookies.get('bgcolor')
    fsize = request.cookies.get('fsize')
    bordercolor = request.cookies.get('bordercolor')
    borderwidth = request.cookies.get('borderwidth')
    return render_template('lab3/settings.html', color=color, bgcolor=bgcolor, fsize=fsize, bordercolor=bordercolor, borderwidth=borderwidth)





@lab3.route('/lab3/ticketform')
def ticketform():
    return render_template('lab3/ticketform.html')

@lab3.route('/lab3/ticketresult', methods=['POST', 'GET'])
def ticket():
    fio = request.form['fio']
    shelf = request.form['shelf']
    bedding = 'bedding' in request.form
    baggage = 'baggage' in request.form
    age = int(request.form['age'])
    departure = request.form['departure']
    destination = request.form['destination']
    date = request.form['date']
    insurance = 'insurance' in request.form

    # Проверка на пустые поля
    if not all([fio, shelf, age, departure, destination, date]):
        return "Все поля должны быть заполнены!", 400

    # Проверка возраста
    if age < 1 or age > 120:
        return "Возраст должен быть от 1 до 120 лет!", 400

    # Расчет стоимости билета
    base_price = 700 if age < 18 else 1000
    if shelf in ['нижняя', 'нижняя боковая']:
        base_price += 100
    if bedding:
        base_price += 75
    if baggage:
        base_price += 250
    if insurance:
        base_price += 150

    return render_template('lab3/ticketresult.html', fio=fio, shelf=shelf, bedding=bedding, baggage=baggage, age=age,
                        departure=departure, destination=destination, date=date, insurance=insurance, price=base_price)
    
    
    
@lab3.route('/lab3/settings/clear_cookies')
def clear_cookies():
    resp = make_response(redirect('/lab3/settings/'))
    resp.delete_cookie('color')
    resp.delete_cookie('bgcolor')
    resp.delete_cookie('fsize')
    resp.delete_cookie('bordercolor')
    resp.delete_cookie('borderwidth')
    return resp




# Список товаров
products = [
    {"name": "Футболка", "price": 1000, "brand": "Nike", "size": "M"},
    {"name": "Джинсы", "price": 3000, "brand": "Levi's", "size": "32"},
    {"name": "Куртка", "price": 13000, "brand": "The North Face", "size": "L"},
    {"name": "Шорты", "price": 500, "brand": "Adidas", "size": "S"},
    {"name": "Платье", "price": 200, "brand": "Zara", "size": "M"},
    {"name": "Ботинки", "price": 20000, "brand": "Timberland", "size": "42"},
    {"name": "Рубашка", "price": 3250, "brand": "Ralph Lauren", "size": "L"},
    {"name": "Свитер", "price": 700, "brand": "Gucci", "size": "XL"},
    {"name": "Шляпа", "price": 1000, "brand": "New Era", "size": "M"},
    {"name": "Пальто", "price": 170, "brand": "Burberry", "size": "L"},
    {"name": "Брюки", "price": 3000, "brand": "Calvin Klein", "size": "34"},
    {"name": "Кроссовки", "price": 15000, "brand": "Puma", "size": "41"},
    {"name": "Юбка", "price": 700, "brand": "H&M", "size": "S"},
    {"name": "Футболка", "price": 600, "brand": "Under Armour", "size": "L"},
    {"name": "Джемпер", "price": 700, "brand": "Tommy Hilfiger", "size": "M"},
    {"name": "Шорты", "price": 500, "brand": "Reebok", "size": "M"},
    {"name": "Платье", "price": 190, "brand": "Mango", "size": "S"},
    {"name": "Ботинки", "price": 23000, "brand": "Dr. Martens", "size": "43"},
    {"name": "Рубашка", "price": 1900, "brand": "Hugo Boss", "size": "L"},
    {"name": "Свитер", "price": 1000, "brand": "Armani", "size": "XL"}
]

@lab3.route('/lab3/productss')
def productss():
    return render_template('lab3/productss.html')

@lab3.route('/lab3/results', methods=['POST', 'GET'])
def search():
    min_price = float(request.form['min_price'])
    max_price = float(request.form['max_price'])
    filtered_products = [product for product in products if min_price <= product['price'] <= max_price]
    return render_template('lab3/result.html', products=filtered_products)