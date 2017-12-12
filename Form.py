from wtforms import Form, BooleanField, StringField, PasswordField, validators


class SignupForm(Form):
    first_name = StringField('first_name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    last_name = StringField('last_name', [validators.DataRequired(), validators.Length(min=4, max=25)])
    email = StringField('email', [validators.DataRequired, validators.Length(min=6, max=35),
                                  validators.EqualTo('confirm_email', message='Email does not match')])
    confirm_email = StringField('confirm_email', [validators.DataRequired(), validators.Length(min=4, max=25)])
    password = PasswordField('password', [
        validators.DataRequired(),
        validators.EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('confirm_password', [validators.DataRequired()])
