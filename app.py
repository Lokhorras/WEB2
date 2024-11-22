from flask import Flask, url_for, redirect, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6

from rgz import rgz
import sqlite3
from os import path 
import os
app = Flask(__name__)

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'Секрет')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(rgz)
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
                <ol> <a href="/rgz/"> rgz </a> </ol>
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