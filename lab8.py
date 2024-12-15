from flask import Blueprint, url_for, redirect, render_template, request, session, current_app, jsonify, abort
from werkzeug.security import check_password_hash, generate_password_hash
from psycopg2.extras import RealDictCursor
import psycopg2
import sqlite3
from os import path 
import os
from datetime import datetime

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def main():
    return render_template('lab8/lab8.html')