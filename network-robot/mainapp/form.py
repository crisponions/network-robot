from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, SelectField, validators, FieldList, FormField

class SwitchForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    hostname = StringField('Hostname', validators=[validators.DataRequired()])

    submit = SubmitField('Submit')

class ConfigForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired()])
    password = PasswordField('Password', validators=[validators.DataRequired()])
    hostname = StringField('Hostname', validators=[validators.DataRequired()])
    engineer = StringField('Your Name', validators=[validators.DataRequired()])
    license1 = StringField('License')
    uplink = SelectField('Select Uplink Interface Type', choices=[('xe', 'TenGig'), ('ge', 'Gigabit')], default='xe')
    submit = SubmitField('Submit')

class CustomConfigFormEntries(FlaskForm):
    vlan_id = StringField()
    vlan_name = StringField()

class CustomConfigForm(FlaskForm):
    vlans = FieldList(FormField(CustomConfigFormEntries), min_entries=1)
    submit = SubmitField('Submit')

