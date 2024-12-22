from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        return render_template('lab9/index.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        return redirect(url_for('lab9.age', name=name))

@lab9.route('/lab9/age/<name>', methods=['GET', 'POST'])
def age(name):
    if request.method == 'GET':
        return render_template('lab9/age.html', name=name)
    elif request.method == 'POST':
        age = request.form.get('age')
        return redirect(url_for('lab9.gender', name=name, age=age))

@lab9.route('/lab9/gender/<name>/<age>', methods=['GET', 'POST'])
def gender(name, age):
    if request.method == 'GET':
        return render_template('lab9/gender.html', name=name, age=age)
    elif request.method == 'POST':
        gender = request.form.get('gender')
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))

@lab9.route('/lab9/preference/<name>/<age>/<gender>', methods=['GET', 'POST'])
def preference(name, age, gender):
    if request.method == 'GET':
        return render_template('lab9/preference.html', name=name, age=age, gender=gender)
    elif request.method == 'POST':
        preference = request.form.get('preference')
        return redirect(url_for('lab9.detail', name=name, age=age, gender=gender, preference=preference))

@lab9.route('/lab9/detail/<name>/<age>/<gender>/<preference>', methods=['GET', 'POST'])
def detail(name, age, gender, preference):
    if request.method == 'GET':
        return render_template('lab9/detail.html', name=name, age=age, gender=gender, preference=preference)
    elif request.method == 'POST':
        detail = request.form.get('detail')
        return render_template('lab9/congratulation.html', name=name, age=age, gender=gender, preference=preference, detail=detail)