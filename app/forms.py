from flask_wtf import Form
from wtforms import SelectField
from wtforms.validators import Optional


class SelectTheme(Form):
    theme = SelectField("Theme", [Optional()], choices=[(f, f) for f in filenames])