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

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods= ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')
    
    login_form = request.form.get('login')
    password_form = request.form.get('password')
    
    login_exists = users.query.filter_by(login='alex').first()
    if login_exists:
        return render_template('lab8/register.html',
                            error = 'Уже такой юзер есть')
    
    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()    