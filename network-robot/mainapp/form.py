from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, validators

class SwitchForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    hostname = StringField('Hostname', validators=[validators.DataRequired()])

    submit = SubmitField('Submit')
