import collections
import logging
import os
from base64 import b64encode
from logging.handlers import RotatingFileHandler

import jinja2
from flask import Flask, render_template, send_from_directory
from flask_misaka import Misaka

from JSONconfig import Config
from page import Page, parse_path

app = Flask(__name__, static_url_path='/static/')
Misaka(app)
cfg = Config("config")
app.jinja_env.cache = {}
site_info = point = collections.namedtuple('Site', ['header', 'subtitle'])
site_info.header = cfg.get("header", "Header Holder")
site_info.subtitle = cfg.get("subtitle", "Subtitle Holder")
# each folder has it's own info.json. says if it is hidden or not? Other details like subnav name?
pages = {}
nav_items = []


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def page(path):
    app.logger.info("Getting page: " + path)
    page_file = get_page(path)

    if page_file is not None:
        app.logger.info("Parsing page")

        return render_template("base.html",
                               content=page_file.markup,
                               nav=nav_items,
                               title=page_file.title,
                               header=site_info.header,
                               subtitle=site_info.subtitle)
    else:
        app.logger.info("Page not found")
        # technically can't happen since Page is returned, containing 404
        return "404"


@app.route('/static/<path:filename>')
def theme_static(filename):
    app.logger.info("Providing static file: " + filename)
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


def gen_navbar():
    # Nav should be generated once, perhaps updated whenever files are detected as updated
    for current_page in os.listdir("pages"):
        current_page = os.path.splitext(current_page)[0]
        page = get_page(current_page)
        if page.time is None:
            continue
        app.logger.info("Got: " + page.title)
        page_dict = {'name': page.title, 'path': '/' + page.name}
        if os.path.isdir("pages/" + current_page) and os.listdir("pages/" + current_page) != []:
            subs = []
            for sub_page in os.listdir("pages/" + current_page):
                app.logger.info("this:" + os.path.splitext(sub_page)[0])
                if os.path.splitext(sub_page)[1] == ".md" and os.path.splitext(sub_page)[0] != "index":
                    app.logger.info("Adding to submenu: " + os.path.splitext(sub_page)[0])
                    subs.append(
                        {'name': get_page(current_page + "/" + sub_page).title, 'path': current_page + '/' + sub_page})
            page_dict["subs"] = subs
        nav_items.append(page_dict)
        app.logger.info(nav_items)


def get_page(path):
    app.logger.info("Getting: " + path)
    if os.path.isdir(parse_path(path, False)):
        path += "/index"
    if path in pages:
        app.logger.info("Cache Hit")
        if os.path.isfile(parse_path(path)) and pages.get(path).time < os.path.getmtime(parse_path(path)):
            app.logger.info("Cache Reloading")
            pages[path] = Page(path)
    else:
        app.logger.info("Cache Miss")
        pages[path] = Page(path)
    return pages.get(path)


@app.before_first_request
def start():
    """
    Load Config with secret key, and current theme.
    """
    app.config['SECRET_KEY'] = cfg.get("secret-key", b64encode(os.urandom(24)).decode('utf-8'))
    app.logger.info("Loaded key: " + app.config['SECRET_KEY'])
    set_theme(cfg.get("theme", "default"))
    gen_navbar()


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
