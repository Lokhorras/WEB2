from flask import Flask, url_for, redirect
app = Flask(__name__)


@app.errorhandler(404)
def not_found(err):
    return "Нет такой страницы", 404


@app.route("/")
def start():

    styles = url_for("static", filename="styles.css")
    return '''<!doctype html>
        <html>
            <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных </header>
            <link rel = "stylesheet" href="''' + styles +'''"    
            <body>
                <h1>НГТУ, ФБ, Лабораторные работы</h1> 
                <ol> <a href="/lab1"> 1 Лабораторная работа </a> </ol>
            </body>
            <footer><p>Студент: Миракин Д.В.</p>
            Группа: ФБИ-22 
            Курс: Ф3
            Год: 2024
            </footer>
        </html>'''



@app.route("/lab1/web")
def web():
    return """<!doctype html> 
        <html> 
            <body> 
                <h1>web-сервер на flask</h1> 
                <a href="/lab1/author">author</a> 
            </body> 
        </html>""", 200, {
                'X-Server': 'sample',
                'Content-Type': 'text/plain; charset=utf-8'
        }


@app.route("/lab1/author")
def author():
    name = "Миракин Д.В."
    group = "ФБИ-22"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>  
                <p>Факультет: """ + faculty + """</p>  
                <a href="/lab1/web">web</a>
            </body> 
        </html>"""
        
        
@app.route("/lab1/oak")
def oak():
    path = url_for("static", filename="1.jpg")
    lab1 = url_for("static", filename="lab1.css")
    return '''
<!doctype html>
<html>
    <link rel = "stylesheet" href="''' + lab1 +'''"
    <body>
        <h1>Дуб</h1>
        <img src="''' + path +'''">
    </body>
</html>
'''
count = 0 
@app.route('/lab1/counter')
def counter():
    global count
    count += 1 
    return '''
<!doctype html>
<html>
    <body>
        <a href="/lab1/clear">Очищение</a>
        Cколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
'''


@app.route('/lab1/clear')
def clear():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
    <a href="/lab1/counter">Очистка</a>
    </body>
</html>
'''


@app.route('/lab1/info')
def info():
    return redirect('/lab1/info')

@app.route('/lab1/created')
def created():
    return '''
<!doctype html>
<html>
    <body>
        <h1>Cоздано успешно</h1>
        <div><i>что-то задано...</i></div>
    </body>
</html>
''', 201


@app.route('/lab1')
def lab1():
        styles = url_for("static", filename="styles.css")
        return '''
<!doctype html>
<html>
    <link rel = "stylesheet" href="''' + styles +'''"    
    <title> Лаба 1 </title>
    <body>
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <a href="/">Корень сайта</a>
    </body>
</html>
'''





@app.route('/error/400')
def error_400():
    return 'Bad Request', 400

@app.route('/error/401')
def error_401():
    return 'Unauthorized', 401

@app.route('/error/402')
def error_402():
    return 'Payment Required', 402

@app.route('/error/403')
def error_403():
    return 'Forbidden', 403

@app.route('/error/405')
def error_405():
    return 'Method Not Allowed', 405

@app.route('/error/418')
def error_418():
    return "I'm a teapot", 418