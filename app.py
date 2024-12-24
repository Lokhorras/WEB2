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
from rgz2 import rgz2
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
app.register_blueprint(rgz2)

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
    return '''<!doctype html>
        <html>
            <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных </header>
            <link rel = "stylesheet" href="''' + styles +'''"   
            <body>
                <h1>НГТУ, ФБ, Лабораторные работы</h1> 
                <ol> <a href="/lab1"> 1 Лабораторная работа </a> </ol>
                <ol> <a href="/lab2"> 2 Лабораторная работа </a> </ol>
                <ol> <a href="/lab3/"> 3 Лабораторная работа </a> </ol>
                <ol> <a href="/lab4/"> 4 Лабораторная работа </a> </ol>
                <ol> <a href="/lab5/"> 5 Лабораторная работа </a> </ol>
                <ol> <a href="/lab6/"> 6 Лабораторная работа </a> </ol>
                <ol> <a href="/lab7/"> 7 Лабораторная работа </a> </ol>
                <ol> <a href="/lab8/"> 8 Лабораторная работа </a> </ol>
                <ol> <a href="/lab9/"> 9 Лабораторная работа </a> </ol>
                <ol> <a href="/rgz/"> rgz </a> </ol>
                <ol> <a href="/rgz2/"> РГЗ </a> </ol>
            </body>
            <footer><p>Студент: Миракин Д.В.</p>
            Группа: ФБИ-22 
            Курс: Ф3
            Год: 2024
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