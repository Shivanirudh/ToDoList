from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,validators,DateField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('New Password', [validators.Required(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Re-enter Password')
    accept_tos = BooleanField('I accept the Terms of Service and Privacy Notice', [validators.Required()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class TaskForm(FlaskForm):
    task = StringField('Task name', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = StringField('Status',validators=[DataRequired()])
    submit = SubmitField('Add task')

class ModForm(FlaskForm):
    task = StringField('Task to be modified', validators=[DataRequired()])
    new_task = StringField('New Task name', validators=[DataRequired()])
    due_date = DateField('Due Date', format='%Y-%m-%d', validators=[DataRequired()])
    status = StringField('Status',validators=[DataRequired()])
    submit = SubmitField('Add task')