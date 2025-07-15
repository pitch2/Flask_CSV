from flask import Flask, request, render_template_string, redirect, url_for, abort, session, render_template, flash
from markupsafe import Markup, escape
import pandas as pd
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = ".\CSV_files"
allowed_extensions = {"csv"}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def affichage_pandas_base():
    return render_template("home.html")

@app.route("/request/<file>")
def request_head_default(file):
    return render_template_string('{{ data|safe }}', data=pd.read_csv(f"./CSV_files/{file}.csv").head(1).to_html())

@app.route("/request/<file>/<int:number_column>")
def request_head_number(file, number_column):
    return render_template_string('{{ data|safe }}', data=pd.read_csv(f"./CSV_files/{file}.csv").head(int(number_column)).to_html())

@app.route("/request/<file>/<column>/<int:number_column>")
def request_attribut(file, column, number_column):
    return render_template_string(((pd.read_csv(fr".\CSV_files\{file}.csv")[[column]]).head(int(number_column))).to_html())

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

@app.route("/listing")
def liste_CSV():
    liste = (' ; '.join(os.listdir("CSV_files")))
    return render_template("liste_CSV.html", liste=liste)

@app.route("/upload_file", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return f"You don't upload file"
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return f"You don't upload file"
        if file and allowed_file(file.filename): #Si ok ->
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename, file)
            return render_template_string('{{ data|safe }}', data=pd.read_csv(f"./CSV_files/{filename.split(".")[0]}.csv").head(1).to_html())
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

# Ajout des erreurs -> HTML
# Ajout d'une visualisation au moment de l'upload
# Autre fonction Pandas