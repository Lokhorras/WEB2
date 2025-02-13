from flask import Flask, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from db.models import users
from flask_login import LoginManager
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz
from db import db
import sqlite3
from os import path 
import os
app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))


app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Секретно-секретный секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'danil123'
    db_user = 'danil123'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = \
        f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "danil123.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'

db.init_app(app)


    
deleted = False
create = False


@app.route("/")
def start():
    styles = url_for("static", filename="lab1/styles.css")
    return f'''<!doctype html>
        <html>
            <head>
                <title>НГТУ, ФБ, WEB-программирование</title>
                <link rel="stylesheet" href="{styles}">
            </head>
            <body>
                <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</header>
                <h1>НГТУ, ФБ, Лабораторные работы</h1> 
                <table border="1" cellspacing="0" cellpadding="10">
                    <tr>
                        <th>№</th>
                        <th>Название</th>
                        <th>Ссылка</th>
                    </tr>
                    <tr><td>1</td><td>Лабораторная работа 1</td><td><a href="/lab1">Перейти</a></td></tr>
                    <tr><td>2</td><td>Лабораторная работа 2</td><td><a href="/lab2">Перейти</a></td></tr>
                    <tr><td>3</td><td>Лабораторная работа 3</td><td><a href="/lab3">Перейти</a></td></tr>
                    <tr><td>4</td><td>Лабораторная работа 4</td><td><a href="/lab4">Перейти</a></td></tr>
                    <tr><td>5</td><td>Лабораторная работа 5</td><td><a href="/lab5">Перейти</a></td></tr>
                    <tr><td>6</td><td>Лабораторная работа 6</td><td><a href="/lab6">Перейти</a></td></tr>
                    <tr><td>7</td><td>Лабораторная работа 7</td><td><a href="/lab7">Перейти</a></td></tr>
                    <tr><td>8</td><td>Лабораторная работа 8</td><td><a href="/lab8">Перейти</a></td></tr>
                    <tr><td>9</td><td>Лабораторная работа 9</td><td><a href="/lab9">Перейти</a></td></tr>
                    <tr><td>10</td><td>РГЗ</td><td><a href="/rgz">Перейти</a></td></tr>
                </table>
            </body>
            <footer>
                <p>Студент: Перевязко Алина</p>
                <p>Группа: ФБИ-21</p>
                <p>Курс: Ф3</p>
                <p>Год: 2024</p>
            </footer>
        </html>'''


@app.errorhandler(404)
def not_found(err):
    hm = url_for("static", filename="lab1/тяжелыйметалл.jpg")
    styles = url_for("static", filename="lab1/styles.css")
    lab1 = url_for("static", filename="lab1.css")
    return '''<!doctype html>
        <html>
            <header>Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал</header>
            <link rel = "stylesheet" href="''' + lab1 +'''"  
            <link rel = "stylesheet" href="''' + styles +'''"    
            <body>
                <h1>Тяжелый металл</h1>     
                <img src="''' + hm +'''">
            </body>
            <footer><p>Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал</p></footer>
        </html>''', 404


@app.errorhandler(500)
def not_found(err):
    return '''
        <h1>Ошибка сервера</h1>
        <p>Извините, произошла ошибка на сервере. Пожалуйста, попробуйте позже.</p>
    ''', 500