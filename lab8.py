from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os
from datetime import datetime
from db import db
from db.models import users, articles 
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('/lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form:
        return render_template('/lab8/register.html', error = 'Заполните все поля!')

    if not password_form:
        return render_template('/lab8/register.html', error = 'Заполните все поля!')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('/lab8/register.html', error = 'Такой пользователь уже существует')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    login_user(new_user, remember=False)

    return redirect('/lab8/login')



@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('/lab8/login.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    remember_me = request.form.get('remember_me')

    if not login_form:
        return render_template('/lab8/login.html', error = 'Заполните все поля!')

    if not password_form:
        return render_template('/lab8/login.html', error = 'Заполните все поля!')

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember_me == True)
            return redirect('/lab8/')
        
    return render_template('/lab8/login.html', error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    return 'Список статей'
    
@lab8.route('/lab8/logout')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')

@lab8.route('/lab8/create_article', methods=['GET', 'POST'])
@login_required
def create_article():
    if request.method == 'POST':
        # Получаем данные из формы
        title = request.form.get('title')
        article_text = request.form.get('article_text')
        is_public = request.form.get('is_public') == 'on'  # Проверяем, отмечена ли галочка

        # Создаем новую статью
        new_article = articles(
            login_id=current_user.id,
            title=title,
            article_text=article_text,
            is_public=is_public
        )

        # Добавляем статью в базу данных
        db.session.add(new_article)
        db.session.commit()

        return redirect('/lab8/') 

    return render_template('/lab8/create_article.html')

@lab8.route('/lab8/articles')
@login_required
def articles_list():
    # Получаем статьи текущего пользователя
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    return render_template('/lab8/articles_list.html', articles=user_articles)

@lab8.route('/lab8/delete_article/<int:article_id>', methods=['POST'])
@login_required
def delete_article(article_id):
    article = articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        abort(403)  # Запрещаем удаление статьи другого пользователя

    db.session.delete(article)
    db.session.commit()
    return redirect('/lab8/') 

@lab8.route('/lab8/edit_article/<int:article_id>', methods=['GET', 'POST'])
@login_required
def edit_article(article_id):
    article = articles.query.get_or_404(article_id)
    if article.login_id != current_user.id:
        abort(403)  # Запрещаем редактирование статьи другого пользователя

    if request.method == 'POST':
        article.title = request.form.get('title')
        article.article_text = request.form.get('article_text')
        article.is_public = request.form.get('is_public') == 'on'
        db.session.commit()
        return redirect('/lab8/') 

    return render_template('/lab8/edit_article.html', article=article)