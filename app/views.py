import os
from os import listdir
from os.path import isfile, join
from flask import render_template, flash, redirect, request, url_for
from werkzeug import secure_filename
from app import app
from .forms import AdminForm


@app.route("/")
def index():
    return render_template("index.html",
                           title='Home',
                           current_css=app.config['CURRENT_CSS'])


@app.route("/admin", methods=['GET', 'POST'])
def admin():
    # Lists all css files in the static/stylesheets folder
    choices_list = (f for f in listdir('./app/static/stylesheets')
                    if isfile(join('./app/static/stylesheets/', f)))
    # Makes it into an array that wtforms can read
    choices = []
    for choice in choices_list:
        choices.append((choice, choice))

    # Create the admin form using the class made in forms.py
    adminForm = AdminForm()
    adminForm.choice_list.choices = choices

    # Render the template
    return render_template("admin.html",
                           title="Control Panel",
                           current_css=app.config['CURRENT_CSS'],
                           adminForm=adminForm)


@app.route("/adminAction", methods=['POST'])
def uploadStylesheet():
    try:
        # get the form so we can get its data and such
        adminForm = AdminForm()

        # If user has selected a file, upload it. Otherwise don't do anything
        if adminForm.template_change_box.data.filename is not '':
            file = request.files['template_change_box']
            if file is not '':
                filename = secure_filename(file.filename)
                if filename.rsplit('.', 1)[1] == "css":
                    if file:
                        file.save(os.path.join(app.config['CSS_UPLOAD_FOLDER'],
                                               filename))
                        flash("succesful upload")
                else:
                    flash("that's not a css file")

        # If the user has chosen a css file different from the current one,
        # set the current one from the app config to the new one
        if adminForm.choice_list.data is not app.config['CURRENT_CSS']:
            app.config['CURRENT_CSS'] = adminForm.choice_list.data
            flash('CSS Updated successfully')

    except Exception as err:
        flash("Error: " + str(err))
    return redirect(url_for('admin'))
