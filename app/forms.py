from flask_wtf import Form
from wtforms import SelectField
from wtforms.validators import Optional
from app import list_themes


themes = list_themes()


class SelectTheme(Form):
    theme = SelectField("Theme", choices=[(t, t) for t in themes])