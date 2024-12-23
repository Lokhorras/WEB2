from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os
from datetime import datetime

lab7 = Blueprint('lab7', __name__)


def get_db_connection():
    conn = psycopg2.connect(
        host = '127.0.0.1',
        database = 'one',
        user = 'one',
        password = '123'
    )
    return conn


@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM films ORDER BY id;")
        films = cursor.fetchall()
    conn.close()
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    conn = get_db_connection()
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT * FROM films WHERE id = %s;", (id,))
        film = cursor.fetchone()
    conn.close()
    if not film:
        return jsonify({"error": "Фильм не найден"}), 404
    return jsonify(film)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def delete_film(id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM films WHERE id = %s RETURNING id;", (id,))
        deleted_id = cursor.fetchone()
        if not deleted_id:
            conn.close()
            return jsonify({"error": "Такого фильма нет"}), 404
        conn.commit()
    conn.close()
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def update_film(id):
    updated_film = request.get_json()

    if not updated_film.get('title_ru') or not updated_film['title_ru'].strip():
        return jsonify({"error": "Название фильма на русском обязательно"}), 400

    if not updated_film.get('year') or not isinstance(updated_film['year'], int):
        return jsonify({"error": "Год выпуска обязателен и должен быть числом"}), 400
    
    if updated_film['year'] < 1895 or updated_film['year'] > datetime.now().year:
        return jsonify({"error": "Год выпуска должен быть от 1895 до текущего"}), 400

    if not updated_film.get('description') or len(updated_film['description']) > 2000:
        return jsonify({"error": "Описание обязательно и не должно превышать 2000 символов"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            UPDATE films 
            SET title = %s, title_ru = %s, year = %s, description = %s, updated_at = CURRENT_TIMESTAMP 
            WHERE id = %s RETURNING id;
            """,
            (updated_film.get('title'), updated_film['title_ru'], updated_film['year'], updated_film['description'], id)
        )
        updated_id = cursor.fetchone()
        if not updated_id:
            conn.close()
            return jsonify({"error": "Такого фильма нет"}), 404
        conn.commit()
    conn.close()
    return jsonify({"id": id}), 200

    

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    new_film = request.get_json()
    
    if not new_film.get('title_ru') or not new_film['title_ru'].strip():
        return jsonify({"error": "Название фильма на русском обязательно"}), 400

    if not new_film.get('year') or not isinstance(new_film['year'], int):
        return jsonify({"error": "Год выпуска обязателен и должен быть числом"}), 400
    
    if new_film['year'] < 1895 or new_film['year'] > datetime.now().year:
        return jsonify({"error": "Год выпуска должен быть от 1895 до текущего"}), 400

    if not new_film.get('description') or len(new_film['description']) > 2000:
        return jsonify({"error": "Описание обязательно и не должно превышать 2000 символов"}), 400

    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            """
            INSERT INTO films (title, title_ru, year, description) 
            VALUES (%s, %s, %s, %s) RETURNING id;
            """,
            (new_film.get('title'), new_film['title_ru'], new_film['year'], new_film['description'])
        )
        new_id = cursor.fetchone()[0]
        conn.commit()
    conn.close()
    return jsonify({"id": new_id}), 201
