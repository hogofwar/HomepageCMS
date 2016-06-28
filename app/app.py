import jinja2, sys, os
from JSONconfig import Config
from forms import *
from flask import Flask, render_template, send_from_directory, request

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_url_path='')
#app.config.from_object('config')

cfg = Config()
app.config['SECRET_KEY'] = '<the super secret key comes here>'

@app.route('/static/<path:filename>')
def theme_static(filename):
    if os.path.isfile(app.root_path + "/themes/%s/static/%s" % (cfg.get("theme"), filename)):
        return send_from_directory(app.root_path + "/themes/%s/static/" % cfg.get("theme"), filename)
    return send_from_directory(app.root_path + "/themes/default/static/", filename)


@app.route("/")
def index():
    return render_template("base.html",
                           title='Home')


@app.route("/admin")
def admin():
    form = SelectTheme(request.form)
    return render_template("admin.html",
                           title='Admin',
                           form=form)


# @app.errorhandler(404)
# def not_found_error(error):
#     # Let user configure 404 page
#     return render_template('errors/404.html'), 404


@app.before_first_request
def start():
    cfg.load()

    app.config['SECRET_KEY'] = cfg.get("secret-key")
    app.logger.info(cfg.get("secret-key"))
    set_theme(cfg.get("theme"))


def list_themes():
    theme_folders = []
    for folder in os.listdir("themes"):
        if os.path.isdir(os.path.join("themes", folder)):
            theme_folders.append(folder)
    return theme_folders


def set_theme(theme):
    theme_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['themes/%s/templates/' % theme,
                                 'themes/default/templates/']),
    ])
    app.jinja_loader = theme_loader


if __name__ == '__main__':
    handler = RotatingFileHandler('foo.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
