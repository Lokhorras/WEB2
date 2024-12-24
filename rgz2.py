from flask import Blueprint, jsonify, request, session, redirect, render_template
import sqlite3
from os import path

rgz2 = Blueprint('rgz2', __name__)

def db_connect():
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "database.db")
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    return conn, cur

def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

@rgz2.route('/rgz2/')
def mainn():
    return render_template('rgz2/index.html')