from Model import DBSingleton, SignUp
from Form import SignupForm
from flask import Flask, render_template, redirect, session, request, flash, url_for, jsonify
import sys
import os
sys.path.append(os.getcwd())


app = Flask(__name__)


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
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = SignUp(first_name=form.first_name.data, last_name=form.last_name.data, email=form.email.data,
                      confirm_email=form.confirm_email.data, password=form.password.data,
                      confirm_password=form.confirm_password.data)
        user.save()
        flash('You have successfully signed up')
        return redirect(url_for('dashboard.html'))

    return render_template('index.html', form=form)



