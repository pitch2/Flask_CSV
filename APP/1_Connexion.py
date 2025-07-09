from flask import Flask, request, render_template, redirect, url_for, abort, session
from markupsafe import Markup, escape
import pandas as pd

df = pd.read_csv('.\eletric_car.csv')
c = df[["brand","model"]]
print(c.head())

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8zec]/'

@app.route("/")
def index():
    if 'username' in session:
        return f"Salut {session["username"]} sur la page de base, avec le password {session["password"]}"
    else:
        return redirect(url_for("login"))

@app.route("/hub/<string:num>")
def hub(num):
    try:
        if int(num) == 50:
            return render_template("hello.html", title=num, texte=f"Coucou {num}")
        else:
            abort(404)
    except ValueError:
        abort(404)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html"), 404

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        session['password'] = request.form['password']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=password name=password>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))