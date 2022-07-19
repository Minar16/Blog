from flask import Flask, redirect, request, url_for, render_template

app = Flask(__name__)

@app.route ('/')
def index():
    return render_template("index.html")

@app.route ('/user/<name>')
def user(name):
    return "<h1>Good {}!</h1>".format(name)




if __name__ == "__main__":
    app.run()
