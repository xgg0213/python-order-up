from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired

# class LoginForm(FlaskForm):
#     # Employee Number field
#     employee_number = StringField("Employee number", validators=[DataRequired()])
    
#     # Password field
#     password = PasswordField("Password", validators=[DataRequired()])
    
#     # Submit button
#     submit = SubmitField("Login")

class TableAssignmentForm(FlaskForm):
    tables = SelectField("Tables", coerce=int)
    servers = SelectField("Servers", coerce=int)
    assign = SubmitField("Assign")

class MenuItemAssignmentForm(FlaskForm):
    menu_item_ids = SelectMultipleField("Menu items", coerce=int)