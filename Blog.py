from crypt import methods
import email
from enum import unique
from flask import Flask, redirect, request, url_for, render_template, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email, Length
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime



app = Flask(__name__)
app.config['SECRET_KEY'] = "0Minar16"

Bootstrap(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlte:///users.db'

# db = SQLAlchemy(app)

class NameForm(FlaskForm):
    name = StringField("What's Your Name", validators=[InputRequired(), Length(min=6, max=15)])
    submit = SubmitField("Submit")

# class RegForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired(), Length(min=6, max=15)])
#     email = StringField('email', validators=[InputRequired(), Length(max=100)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=15)])
#     submit = SubmitField("Submit")




# @app.route ('/')
# def index():
#     return render_template("index.html")

# @app.route ('/user/<name>')
# def user(name):
#     return "<h1>Good {}!</h1>".format(name)

@app.route ('/')
def index():
    return render_template("index.html")

@app.route ('/name', methods = ['GET', 'POST'])
def name():
    name = None
    form = NameForm()

    if form.validate_on_submit():
        name = form.name.data
        form.name.data = ''

    return render_template("log.html", name = name, form = form)




if __name__ == "__main__":
    app.run()
