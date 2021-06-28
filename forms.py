from flask_wtf import FlaskForm
from wtforms import StringField,TextField,SubmitField,IntegerField
from wtforms.validators import DataRequired,Length,Email

class AccountForm(FlaskForm):
  code=StringField('Code',validators=[DataRequired()])
  submit=SubmitField('Submit')