from wtforms import Form, BooleanField, StringField, PasswordField, validators


class SignupForm(Form):
    first_name = StringField('First Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    last_name = StringField('Last Name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.DataRequired(), validators.Length(min=6, max=100),
                                  validators.EqualTo('confirm_email', message='Email does not match')])
    confirm_email = StringField('Confirm Email', [validators.DataRequired(), validators.Length(min=4, max=100)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('Confirm Password', [validators.DataRequired()])
