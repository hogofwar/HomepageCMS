from flask_wtf import Form
from wtforms import SelectField


class SelectTheme(Form):
   ## theme = SelectField(u"Filename", [Optional()], choices=[(f, f) for f in filenames])