from flask import Blueprint, url_for, redirect, render_template, request, session, current_app
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
    return (films)

@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return ({"error": "Такого фильма нет"}), 404
    return (films[id])


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return ({"error": "Такого фильма нет"}), 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return ({"error": "Такого фильма нет"}), 404
    film = request.get_json()
    films[id] = film
    return (films[id])


@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_films():
    new_film = request.get_json()
    films.append(new_film)
    new_film_index = len(films) - 1
    return ({"index": new_film_index}), 201