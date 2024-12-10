from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')

films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кристофер Нолан создал эпический научно-фантастический фильм о раздвоении личности и погружении в сны."
    },
    {
        "title": "The Matrix",
        "title_ru": "Матрица",
        "year": 1999,
        "description": "Фильм о реальности, иллюзиях и борьбе человека против машин, управляющих миром."
    },
    {
        "title": "Interstellar",
        "title_ru": "Интерстеллар",
        "year": 2014,
        "description": "Фильм о космических путешествиях и поиске новой планеты для человечества, находящегося на грани вымирания."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return jsonify(films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Такого фильма нет"}), 404
    return jsonify(films[id])

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Такого фильма нет"}), 404
    del films[id]
    return '', 204

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return jsonify({"error": "Такого фильма нет"}), 404
    
    updated_film = request.get_json()

    # Проверка на пустое описание
    if 'description' in updated_film and updated_film['description'] == '':
        return jsonify({'error': 'Заполните описание'}), 400
    
    # Если оригинальное название пустое, присваиваем русское название
    if 'title' in updated_film and updated_film['title'] == '' and 'title_ru' in updated_film:
        updated_film['title'] = updated_film['title_ru']

    films[id] = updated_film
    return jsonify(films[id])


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_films():
    new_film = request.get_json()
    
    # Проверка и заполнение оригинального названия, если оно пустое
    if 'title' in new_film and new_film['title'] == '' and 'title_ru' in new_film:
        new_film['title'] = new_film['title_ru']

    # Проверка обязательных полей
    if 'title_ru' not in new_film or new_film['title_ru'] == '':
        return jsonify({"error": "Название фильма на русском обязательно"}), 400
    
    if 'year' not in new_film or not isinstance(new_film['year'], int):
        return jsonify({"error": "Год выпуска обязателен и должен быть числом"}), 400
    
    films.append(new_film)
    new_film_index = len(films) - 1
    return jsonify({"index": new_film_index}), 201
