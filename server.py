from Model import DBSingleton, SignUp
from Form import SignupForm
from passlib.hash import sha256_crypt
from flask import Flask, render_template, redirect, session, request, flash, url_for, jsonify
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import sys
import os
sys.path.append(os.getcwd())


app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")


app.config['MAIL_SERVER'] = os.environ.get("MAIL_SERVER")
app.config['MAIL_PORT'] = os.environ.get("MAIL_PORT")
app.config['MAIL_USE_TLS'] = os.environ.get("MAIL_USE_TLS")
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")


mail = Mail(app)

s = URLSafeTimedSerializer(app.secret_key)


@app.before_first_request
def initialize_tables():
    connect_db()
    if not SignUp.table_exists():
        print("creating table")
        SignUp.create_table()
    else:
        print("exists")
    disconnect_db()


@app.before_request
def connect_db():
    DBSingleton.get_instance().connect()


@app.teardown_request
def disconnect_db(err=None):
    DBSingleton.get_instance().close()


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = SignUp(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                      password=sha256_crypt.encrypt(str(form.password.data)))
        user.save()
        email = str(form.email.data)
        token = s.dumps(email, salt='confirm-email')

        msg = Message('Confirm Email', sender='draogtech@gmail.com', recipients=[email])
        link = url_for('confirm_email', token=token, _external=True)
        msg.body = 'Please click on the link or copy paste on your browser to activate account {}'.format(link)
        mail.send(msg)

        flash('You have successfully signed up. To activate account, please click on link sent to registered email',
              'success')
        return redirect(url_for('register'))

    return render_template('register.html', form=form)


@app.route("/confirm_email/<token>")
def confirm_email(token):
    try:
        email = s.loads(token, salt='confirm-email', max_age=3600)
    except SignatureExpired:
        return 'Signature is expired'
    user = SignUp.update(confirm_email='Yes').where(SignUp.email == 'draogtech@gmail.com')
    user.execute()
    flash('Your account has been activated, you can sign-in now!',
          'success')
    return redirect(url_for('register'))
