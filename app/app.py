import os
from os import listdir
from os.path import isfile, join
from flask import Flask, render_template, flash, redirect, request, url_for

app = Flask(__name__)
app.config.from_object('config')


@app.route("/")
def index():
    return render_template("index.html",
                           title='Home',
                           current_css=app.config['CURRENT_CSS'])


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
