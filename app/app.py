import jinja2, sys, os, re
from flask import url_for
from flask_misaka import Misaka, markdown

from JSONconfig import Config
from page import Page
from flask import Flask, render_template, send_from_directory, request

import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__, static_url_path='/static/')
Misaka(app)
cfg = Config()
app.jinja_env.cache = {}


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def page(path):
    app.logger.info("Checking if page :"+path)
    page_file = Page(path)

    if page_file is not None:
        app.logger.info("parsing page")

        nav_items = []
        for page in os.listdir("pages"):
            if page.endswith('.md'):
                page_dict = {'type': 'file', 'name': Page(page).title, 'path': '/'+page}
                nav_items.append(page_dict)
            elif os.path.isdir("pages/"+page):
                page_dict = {'type': 'subfolder', 'name': page, 'path': '/'+page}
                nav_items.append(page_dict)

        return render_template("base.html",
                               content=page_file.markup,
                               nav=nav_items,
                               title="Title",
                               header="Header",
                               subtitle="Subtitle")
    else:
        app.logger.info("page not found")
        return "404"

@app.route('/static/<path:filename>')
def theme_static(filename):
    app.logger.info("providing static")
    if os.path.isfile(app.root_path + "/themes/%s/static/%s" % (cfg.get("theme"), filename)):
        return send_from_directory(app.root_path + "/themes/%s/static/" % cfg.get("theme"), filename)
    return send_from_directory(app.root_path + "/themes/default/static/", filename)


@app.route('/favicon.ico')
def favicon():
    return theme_static("favicon.ico")
# Relic of theme switching.
# @app.route("/admin", methods=('GET', 'POST'))
# def admin():
#     form = SelectTheme()
#     if form.validate_on_submit():
#         cfg.set("theme", form.theme.data, True)
#         set_theme(form.theme.data)
#         app.logger.info("Set theme")
#     return render_template("admin.html",
#                            title='Admin',
#                            form=form)

# add metadata parsing for Title, author and date. All optional

@app.before_first_request
def start():
    """
    Load Config with secret key, and current theme.
    """
    cfg.load()

    app.config['SECRET_KEY'] = cfg.get("secret-key")
    app.logger.info(cfg.get("secret-key"))
    set_theme(cfg.get("theme"))


def list_themes():
    """
    Get a list of themes.
    TODO: get the data from the theme.json file.
    :return: list of themes
    """
    theme_folders = []
    for folder in os.listdir("themes"):
        if os.path.isdir(os.path.join("themes", folder)):
            theme_folders.append(folder)
    return theme_folders


def set_theme(theme):
    """
    Sets Jinja to use the given theme's folder.
    :param theme: name of theme folder
    :return:
    """
    theme_loader = jinja2.ChoiceLoader([
        app.jinja_loader,
        jinja2.FileSystemLoader(['themes/%s/templates/' % theme,
                                 'themes/default/templates/']),
    ])
    app.jinja_loader = theme_loader


if __name__ == '__main__':
    handler = RotatingFileHandler('cms.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True)
