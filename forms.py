from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalField, IntegerField,\
    TextAreaField, SelectField, PasswordField,BooleanField
from wtforms.validators import Required    

from wtforms import FieldList
from wtforms import FormField

class LoginForm(FlaskForm):
    username = StringField('Login', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Login')
