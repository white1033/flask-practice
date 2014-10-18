# import the Flask class from the flask module
from flask import Flask, render_template, redirect, url_for, request, session, flash, g
from functools import wraps
import sqlite3
# from mosql.query import select
from mosql.db import Database

# create the application object
app = Flask(__name__)

app.secret_key = "it's a secret"
app.database = "sample.db"


# login required decorator
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrapper


# use decorators to link the function to a url
@app.route('/')
@login_required
def home():
    # return "Hello, World!"  # return a string
    g.db = connect_db()
    with g.db as cur:
        # mosql 0.9.1 not work on Python 3 :P
        # cur.execute(select('posts'))
        cur.execute('SELECT * FROM posts')
        posts = [{'title': row[0], 'description': row[1]} for row in cur.fetchall()]
    return render_template('index.html', posts=posts)


@app.route('/welcome')
def welcome():
    return render_template('welcome.html')  # render a template


# route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)


@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You were just logged out!')
    return redirect(url_for('welcome'))


def connect_db():
    return Database(sqlite3, app.database)
# start the server with the 'run()' method
if __name__ == '__main__':
    app.run(debug=True)
