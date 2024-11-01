from flask import Blueprint, url_for, redirect, render_template, request, session
lab5 = Blueprint('lab5', __name__)

@lab5.route('/lab5/')
def lab5_main():
    name_color = request.cookies.get('name_color')
    name = request.cookies.get('name')
    age = 18
    links = [
        {"url": "1", "text": "/lab5/shablon"},


    ]
    return render_template('/lab5/lab5.html', links=links, name=name, name_color=name_color, age=age)