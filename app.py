from flask import Flask, url_for, redirect, render_template
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
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