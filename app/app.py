import os
import jinja2
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_url_path='')
app.config.from_object('config')
theme = "default"

theme_loader = jinja2.ChoiceLoader([
    app.jinja_loader,
    jinja2.FileSystemLoader(['themes/%s/templates/' % theme,
                             'themes/default/templates/']),
])
app.jinja_loader = theme_loader


@app.route('/base/<path:filename>')
def theme_static(filename):
    return send_from_directory(app.root_path + "/themes/%s/static/" % theme, filename)


@app.route("/")
def index():
    return render_template("index.html",
                           title='Home')


@app.route("/admin")
def admin():
    listThemes()
    return render_template("admin.html",
                           title='Home',
                          )


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404


def listThemes():
    for subdir, dirs, files in os.walk("themes"):
        for file in files:
            print(os.path.join(subdir, file), file=sys.stderr)


if __name__ == '__main__':
    app.run(debug=True)
