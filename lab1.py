from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1', __name__)


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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
        
        
@lab1.route("/lab1/oak")
def oak():
    path = url_for("static", filename="lab1/1.jpg")
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
@lab1.route('/lab1/counter')
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


@lab1.route('/lab1/clear')
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


@lab1.route('/lab1/info')
def info():
    return redirect('/lab1//author')


@lab1.route('/lab1/created')
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



    
@lab1.route('/lab1/routestudent')
def routestudent():
    hm = url_for("static", filename="lab1/тяжелыйметалл.jpg")
    content = '''
<!doctype html>
<html>
    <body>
        <h1>Тяжелый металл</h1>
        <p>Fire Alarm.</p>
        <p>Грязный бит — нужен Мойдодыр-р</p>
        <p>На шее ice — это не water-r</p>
        <p>Мой бро — Дима, но не LAZER</p>
        <p>Dodge Challenger, он sounds like «skrrt»</p>
        <p>V-I-P-E-double-R (Р-р-р)</p>
        <p>V-I-P-E-double-R (Р-р-р)</p>
        <p>9mice & Kai Angel</p>
        <img src="''' + hm +'''">
    </body>
</html>'''
    headers = {
        'Content-Language': 'ru',
        'X-Custom-Header-1': 'HM2',
        'X-Custom-Header-2': 'KAI&MICE'
    }
    return (content, 200, headers)


@lab1.route('/lab1')
def lab():
        styles = url_for("static", filename="lab1/styles.css")
        return '''
<!doctype html>
<html>
    <title> Лаба 1 </title>
    <link rel = "stylesheet" href="''' + styles +'''"    
    <body>
        <header>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных </header>
        <p>Flask — фреймворк для создания веб-приложений на языке
программирования Python, использующий набор инструментов
Werkzeug, а также шаблонизатор Jinja2. Относится к категории так
называемых микрофреймворков — минималистичных каркасов
веб-приложений, сознательно предоставляющих лишь самые базовые возможности.</p>
        <h2>Список роутов</h2>
        <ol>
        <li><a href="/lab1/web">Веб</a></li>
        <li><a href="/lab1/author">Автор</a></li>
        <li><a href="/lab1/oak">ДуБ</a></li>
        <li><a href="/lab1/counter">Не помню чё там</a></li>
        <li><a href="lab1/clear">Очистка</a></li>
        <li><a href="/lab1/created'">created</a></li>
        <li><a href="/lab1/info">Инфа</a></li>
        <li><a href="/error/400">400</a></li>
        <li><a href="/error/401">401</a></li>
        <li><a href="/error/402">402</a></li>
        <li><a href="/error/403">403</a></li>
        <li><a href="/error/404">404</a></li>
        <li><a href="/error/405">405</a></li>
        <li><a href="/error/418">418</a></li>
        <li><a href="/error/500">500</a></li>
        <li><a href="/lab1/routestudent">Навыборстудентатяжелыйметалл</a></li>
        </ol>
        <footer><p>Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал Тяжелый метал</p></footer>
    </body>
</html>
'''   


@lab1.route('/lab1/resourse')
def resourse():
    styles2 = url_for("static", filename="lab1/sctyles2.css")
    Kaktus = url_for("static", filename="lab1/Кактус.jpg")
    Mertviy = url_for("static", filename="lab1/Мертвыйкактус.jpg")
    politiy = url_for("static", filename="lab1/Политыйкактус.jpg")
    global create
    global deleted
    if deleted is False  and create is True:
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>Кактус полит</h1>
                <img src="''' + Kaktus +'''">
                <a href="/lab1/create">Полить</a>
                <a href="/lab1/delete">kill kaktus</a>
            </body>
        </html>
        '''
    elif deleted is True:
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>Кактус зДОХ</h1>
                <img src="''' + Mertviy +'''">
                <a href="/lab1/create">Полить</a>
                <a href="/lab1/delete">kill kaktus</a>
            </body>
        </html>
        '''
    else:
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>Кактус не полит</h1>
                <img src="''' + Kaktus +'''">
                <a href="/lab1/create">Полить</a>
                <a href="/lab1/delete">kill kaktus</a>
            </body>
        </html>
        '''

        
@lab1.route('/lab1/delete')
def delete():
    styles2 = url_for("static", filename="sctyles2.css")
    Kaktus = url_for("static", filename="lab1/Кактус.jpg")
    Mertviy = url_for("static", filename="lab1/Мертвыйкактус.jpg")
    politiy = url_for("static", filename="lab1/Политыйкактус.jpg")
    global deleted
    if deleted is True:
        return '''
        <!doctype html>
        <link rel = "stylesheet" href="''' + styles2 +'''" 
        <html>
            <body>
                <h1>Уже убил, чё ты его мучаешь..</h1>
                <img src="''' + Mertviy +'''">
                <a href="/lab1/resourse">нАзад</a>
            </body>
        </html>'''
    else:
        deleted = True
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>Убит....</h1>
                <img src="''' + Mertviy +'''">
                <a href="/lab1/resourse">нАзад</a>
            </body>
        </html>'''

    
@lab1.route('/lab1/create')
def create():
    styles2 = url_for("static", filename="sctyles2.css")
    Kaktus = url_for("static", filename="lab1/Кактус.jpg")
    Mertviy = url_for("static", filename="lab1/Мертвыйкактус.jpg")
    politiy = url_for("static", filename="lab1/Политыйкактус.jpg")
    global create
    global deleted 
    if deleted is True:
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>

                <h1>Мертвого водой не спасти</h1>
                <img src="''' + Mertviy +'''">
                <a href="/lab1/resourse">нАзад</a>
            </body>
        </html>'''
    elif create is True:
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>Уже полит</h1>
                <img src="''' + politiy +'''">
                <a href="/lab1/resourse">нАзад</a>
            </body>
        </html>'''
    else:
        create = True
        return '''
        <!doctype html>
        <html>
            <link rel = "stylesheet" href="''' + styles2 +'''" 
            <body>
                <h1>ПОЛИТ</h1>
                <img src="''' + politiy +'''">
                <a href="/lab1/resourse">нАзад</a>
            </body>
        </html>'''