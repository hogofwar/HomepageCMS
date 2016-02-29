import os
from flask import render_template, flash, redirect, request, url_for
from werkzeug import secure_filename
from app import app
from .forms import CSSTemplate


@app.route("/")
def index():
    return render_template("index.html",
                           title='Home',
                           current_css=app.config['CURRENT_CSS'])


@app.route("/admin", methods=['GET','POST'])
def admin():
    form = CSSTemplate()
    return render_template("admin.html",
                            title="Control Panel",
                            current_css=app.config['CURRENT_CSS'],
                            form=form)


@app.route("/uploadStylesheet", methods=['POST'])
def uploadStylesheet():
    try:
        form = CSSTemplate()
        file = request.files['template_change_box']
        filename = secure_filename(file.filename)
        if filename.rsplit('.', 1)[1] == "css":
            if file:
                file.save(os.path.join(app.config['CSS_UPLOAD_FOLDER'], filename))
                flash("succesful upload")
        else:
            flash("that's not a css file")
    except Exception as err:
        flash("Error: " + str(err))
    return redirect(url_for('admin'))
