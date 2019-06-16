#! /usr/bin/python3

from flask import (Flask, render_template, redirect, url_for,
                   session, request, flash)

from util import db

app = Flask(__name__)
app.secret_key = 'DONT LOOK!!!!'


@app.route('/')
def home():
    if 'email' in session:
        return render_template('logged_in_index.html')
    return render_template('index.html')


@app.route('/excuse')
def excuse():
    ex = db.getExcuse()
    ex = 'Hehe i didn\'t feel like it'
    if 'email' in session:
        return render_template('logged_in_results.html', excuse=ex,
                               email=session['email'])
    return render_template('results.html', excuse=ex)


@app.route('/create_account')
def create_account():
    return render_template('register.html')


@app.route('/register', methods=["POST"])
def register():
    email = request.form['email']
    password = request.form['password']
    password_check = request.form['password_check']
    success = db.register(email, password, password_check)
    if success:
        flash('Success!')
    else:
        flash('Couldn\'t create account')
    return redirect(url_for('home'))


@app.route('/login', methods=["POST"])
def login():
    email = request.form['email']
    password = request.form['password']
    success = db.login(email, password)
    if success:
        flash('Logged in!')
        session['email'] = email
    else:
        flash('Incorrect credentials!')
    return redirect(url_for('home'))


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop['emaill']
    return redirect(url_for('home'))


@app.route('/my_excuses')
def my_excuses():
    if 'email' not in session:
        return redirect(url_for('home'))
    excuses = db.getMyExcuses(session['email'])
    return render_template('excuses.html', excuses=excuses)


@app.route('/save/<excuse>')
def save_excuse(excuse):
    if 'email' not in session:
        return redirect(url_for('home'))
    db.saveExcuse(session['email'], excuse)
    return redirect(url_for('my_excuses'))


if __name__ == '__main__':
    app.debug = True
    app.run()
