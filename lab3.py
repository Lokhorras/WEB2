from flask import Blueprint, url_for, redirect, render_template
lab3 = Blueprint('lab3', __name__)

@lab3.route('/lab3/')
def lab2_main():
    links = [
        {"url": "/lab3/cookie", "text": "Куки"},

    ]
    return render_template('lab3.html', links=links)
