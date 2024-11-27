from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
import os
from os import path 

lab6 = Blueprint('lab6', __name__)

def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'one',
            user = 'one',
            password = '123'
        )
        cur = conn.cursor(cursor_factory = RealDictCursor)
    else:
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

@lab6.route('/lab6/create')
def add():
    offices = [
        {'number': 1, 'tenant': ''},
        {'number': 2, 'tenant': ''},
        {'number': 3, 'tenant': ''},
        {'number': 4, 'tenant': ''},
        {'number': 5, 'tenant': ''}
    ]
    cur.execute('CREATE TABLE offices(number INT, tenant VARCHAR(255))')
    conn, cur = db_connect()
    for office in offices:
        cur.execute("INSERT INTO offices (number, tenant) VALUES (%s, %s);", (office['number'], office['tenant']))
    conn.commit()
    cur.close()
    conn.close()
    return "Offices added successfully"

@lab6.route('/lab6/')
def main():
    return render_template('lab6/lab6.html')

@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices;")
        offices = cur.fetchall()
        db_close(conn, cur)
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        conn, cur = db_connect()
        cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
        office = cur.fetchone()
        if office['tenant'] != '':
            db_close(conn, cur)
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 2,
                    'message': 'Already booked'
                },
                'id': id
            }

        cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", (login, office_number))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    if data['method'] == 'cancellation':
        office_number = data['params']
        conn = db_connect()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
        office = cur.fetchone()
        if office['tenant'] == '':
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 3,
                    'message': 'Office not booked'
                },
                'id': id
            }
        if office['tenant'] != login:
            cur.close()
            conn.close()
            return {
                'jsonrpc': '2.0',
                'error': {
                    'code': 4,
                    'message': 'Cannot cancel someone else booking'
                },
                'id': id
            }
        cur.execute("UPDATE offices SET tenant = '' WHERE number = %s;", (office_number,))
        conn.commit()
        cur.close()
        conn.close()
        return {
            'jsonrpc': '2.0',
            'result': 'success',
            'id': id
        }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }