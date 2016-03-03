from flask.ext.wtf import Form
from wtforms import FileField, SelectField
from wtforms.validators import DataRequired


class AdminForm(Form):
    template_change_box = FileField('CSS Change')
    choice_list = SelectField('Template List', validators=[DataRequired()])
