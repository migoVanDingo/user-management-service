from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, Regexp

class RegistrationForm(FlaskForm):
    username = StringField(
        'Username',
        validators=[
            InputRequired(),
            Length(min=4, max=20),
            Regexp(r'^[a-zA-Z0-9_]*$', message="Username can only contain letters, numbers, and underscores.")
        ]
    )
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            Length(min=4, message="Password must be at least 4 characters long."),
        ]
    )
