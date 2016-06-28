import jinja2, sys, os
from JSONconfig import Config

from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_url_path='')
#app.config.from_object('config')
cfg = Config()


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
    # list_themes()
    return render_template("admin.html",
                           title='Home')


@app.errorhandler(404)
def not_found_error(error):
    # Let user configure 404 page
    return render_template('errors/404.html'), 404


@app.before_first_request
def start():
    cfg.load()
    app.secret_key = cfg.get("secret-key")
    set_theme(cfg.get("theme"))


def list_themes():
    themes = []
    for subdir, dirs, files in os.walk("themes"):
        for folder in dirs:
            themes.append(folder)
    return themes


def set_theme(theme):
    theme_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['themes/%s/templates/' % theme,
                                 'themes/default/templates/']),
    ])
    app.jinja_loader = theme_loader


if __name__ == '__main__':
    app.run(debug=True)
