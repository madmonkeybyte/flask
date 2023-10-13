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
import json


# config file
with open('config.json') as f:
    config = json.load(f)


# db stuff
class Base(DeclarativeBase):
  pass


db = SQLAlchemy(model_class=Base)


# site
app = Flask(__name__)
app.secret_key = config.get('key')
app.config['UPLOAD_FOLDER'] = config.get('upload_folder')
app.config['MAX_CONTENT_LENGTH'] = config.get('max_content_length')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('dbpath')
ALLOWED_EXTENSIONS = config.get('allowed_extensions')


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
    app.run(config.get('host_address'), port=config.get('host_port'), debug=True)