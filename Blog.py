import re
from collections import UserString
from crypt import methods
import email
from email import message
from email.policy import default
from enum import unique
from unicodedata import name
from click import confirm, password_option
from flask import Flask, redirect, request, url_for, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, EqualTo, Length
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import os


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
SECRET_KEY = os.urandom(32)

app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'postgresql://postgres:0Minar16@localhost:5432/postgres_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db=SQLAlchemy(app)
migrate = Migrate(app, db)
Bootstrap(app)
class Users(db.Model):
    id = db.Column(db.Integer, primary_key='True')
    username = db.Column(db.String(40), nullable = False)
    email = db.Column(db.String(100), nullable = False, unique = True)
    password_hash = db.Column(db.String(500), nullable = False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def password (self):
        raise AttributeError('password is not a readable attribute!')
    
    @password.setter
    def password (self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password (self, password):
        return check_password_hash(self.password_hash, password)
    
class LogForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6, max=15)])
    password_hash = PasswordField("Password", validators=[InputRequired(), Length(min=6, max=15)])
    submit = SubmitField("Login")

class SignForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=6, max=15)])
    email = StringField('Email', validators=[InputRequired(), Length(max=100)])
    password_hash = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=15)])
    password_hash2 = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password_hash')])
    submit = SubmitField("Submit")
      
@app.route ('/')
def index():
    return render_template("index.html")

@app.route ('/login', methods = ['GET', 'POST'])
def login():
    form = LogForm()

    if form.validate_on_submit():
        return '<h1>' + form.username.data+ ' ' + form.password.data + '</h1>'
     

    return render_template("log.html", form = form)

@app.route ('/signup', methods = ['GET', 'POST'])
def signup():
    username = None
    form = SignForm()

    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pw = generate_password_hash(form.password_hash.data, "sha256")
            user = Users(username=form.username.data, email=form.email.data, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
        username = form.username.data
        form.username.data = ''
        form.email.data = ''
        form.password_hash.data = ''
        
    flash("User added successfully!!")
    our_users = Users.query.order_by(Users.date_added)

    return render_template("sign.html", form = form, username = username, our_users = our_users)


@app.route ('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
    form = SignForm()
    name_to_update = Users.query.get_or_404(id)
    if request.method == "POST":
        name_to_update.username = request.form['username']
        name_to_update.email = request.form['email']
        try:
            db.session.commit()
            flash("User updated successfully!!")
            return render_template("update.html",form = form, name_to_update = name_to_update)
        except:
            flash("Error! Looks like there was a problem... Try again later.")
            return render_template("update.html",form = form, name_to_update = name_to_update)
    else:
        return render_template("update.html",form = form, name_to_update = name_to_update)

@app.route ('/delete/<int:id>')
def delete(id):
    user_to_delete = Users.query.get_or_404(id)
    username = None
    form = SignForm()

    try:
        db.session.delete (user_to_delete)
        db.session.commit()
        flash("User deleted Successfully!")
        our_users = Users.query.order_by(Users.date_added)

        return render_template("sign.html", form = form, username = username, our_users = our_users)

    except:
        flash("Woops!! There is a problem in deleting user try again later..")
        our_users = Users.query.order_by(Users.date_added)

        return render_template("sign.html", form = form, username = username, our_users = our_users)

if __name__ == "__main__":
    app.run()
