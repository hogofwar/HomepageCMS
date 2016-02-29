from flask.ext.wtf import Form
from wtforms import FileField
from wtforms.validators import DataRequired


class CSSTemplate(Form):
    template_change_box = FileField('CSS Change', validators=[DataRequired()])
