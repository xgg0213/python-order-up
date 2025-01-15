from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    # Employee Number field
    employee_number = StringField("Employee number", validators=[DataRequired()])
    
    # Password field
    password = PasswordField("Password", validators=[DataRequired()])
    
    # Submit button
    submit = SubmitField("Login")