from flask import Blueprint, render_template, request, redirect, url_for, session

lab9 = Blueprint('lab9', __name__)

@lab9.route('/lab9/', methods=['GET', 'POST'])
def main():
    if request.method == 'GET':
        if 'name' in session:
            return redirect(url_for('lab9.congratulation'))
        return render_template('lab9/index.html')
    elif request.method == 'POST':
        name = request.form.get('name')
        session['name'] = name
        return redirect(url_for('lab9.age'))

@lab9.route('/lab9/age', methods=['GET', 'POST'])
def age():
    if request.method == 'GET':
        if 'age' in session:
            return redirect(url_for('lab9.congratulation'))
        if 'name' not in session:
            return redirect(url_for('lab9.main'))
        return render_template('lab9/age.html', name=session['name'])
    elif request.method == 'POST':
        age = request.form.get('age')
        session['age'] = age
        return redirect(url_for('lab9.gender'))

@lab9.route('/lab9/gender', methods=['GET', 'POST'])
def gender():
    if request.method == 'GET':
        if 'gender' in session:
            return redirect(url_for('lab9.congratulation'))
        if 'name' not in session or 'age' not in session:
            return redirect(url_for('lab9.main'))
        return render_template('lab9/gender.html', name=session['name'], age=session['age'])
    elif request.method == 'POST':
        gender = request.form.get('gender')
        session['gender'] = gender
        return redirect(url_for('lab9.preference'))

@lab9.route('/lab9/preference', methods=['GET', 'POST'])
def preference():
    if request.method == 'GET':
        if 'preference' in session:
            return redirect(url_for('lab9.congratulation'))
        if 'name' not in session or 'age' not in session or 'gender' not in session:
            return redirect(url_for('lab9.main'))
        return render_template('lab9/preference.html', name=session['name'], age=session['age'], gender=session['gender'])
    elif request.method == 'POST':
        preference = request.form.get('preference')
        session['preference'] = preference
        return redirect(url_for('lab9.detail'))

@lab9.route('/lab9/detail', methods=['GET', 'POST'])
def detail():
    if request.method == 'GET':
        if 'detail' in session:
            return redirect(url_for('lab9.congratulation'))
        if 'name' not in session or 'age' not in session or 'gender' not in session or 'preference' not in session:
            return redirect(url_for('lab9.main'))
        return render_template('lab9/detail.html', name=session['name'], age=session['age'], gender=session['gender'], preference=session['preference'])
    elif request.method == 'POST':
        detail = request.form.get('detail')
        session['detail'] = detail
        return redirect(url_for('lab9.congratulation'))

@lab9.route('/lab9/congratulation', methods=['GET', 'POST'])
def congratulation():
    if request.method == 'GET':
        return render_template('lab9/congratulation.html', name=session.get('name'), age=session.get('age'), gender=session.get('gender'), preference=session.get('preference'), detail=session.get('detail'))
    elif request.method == 'POST':
        session.clear()
        return redirect(url_for('lab9.main'))