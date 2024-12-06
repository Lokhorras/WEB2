from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os
lab6 = Blueprint('lab6', __name__)


@lab6.route('/lab5/')
def lab():
    return render_template ('lab5/lab5.html', login=session.get('login'))