#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Frederico Sales
<frederico@fredericosales.eng.br>
2023
"""


# imports
import os
from flask import Flask, flash, send_from_directory
from flask import request, abort, redirect, url_for, render_template, session
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


# variables
PATH = "~/Documents/projects/python/flask/src/site/assets"
UPLOAD_FOLDER = PATH + '/uploads'
ALLOWED_EXTENSIONS = { 'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif' }

# db stuff
class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


# site
app = Flask(__name__)
app.secret_key = b'b8ebc09828cbf127f1b961a5384064e0a95a86a21376f337a567768b5b79e182'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///~/Documents/projects/python/flask/src/site/data/site.db"


@app.route("/")
def main():
    """
    """
    if 'username' in session:
        usr = session['username']
    else:
        usr = None
    return render_template('home.html')


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('download_file', name=filename))
    return """
    <!doctype html>
    <html>
    <head>
        <title>Upload a new file</title>
    </head>
    <body>
        <div>
            <h1>Upload a new file</h1>
        </div>
        <div>
            <form method=post enctype=multipart/form-data>
                <div>
                    <input type=file name=file />
                </div>
                <div>
                    <input type=submit value=upload />
                </div>
            </form>
        </div>
    </body>
    </html>
    """


@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)


if __name__ == '__main__':
    app.run('0.0.0.0', port=8000, debug=True)