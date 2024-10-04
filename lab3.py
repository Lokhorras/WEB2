from flask import Blueprint, url_for, redirect, render_template, request, make_response
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab3_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    links = [
        {"url": "/lab3/cookie", "text": "Куки"},
        {"url": "/lab3/del_cookie", "text": "delete_cookies"},
    ]
    return render_template('lab3.html', links=links, name=name, name_color=name_color)

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