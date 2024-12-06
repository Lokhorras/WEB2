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
    return render_template ('lab7/index.html')