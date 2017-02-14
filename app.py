from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    """This function implements sign_in"""
    return render_template("index.html")

@app.route('/signin')
def sign_in():
    """This function implements sign_in"""
    return render_template("signin.html")

@app.route('/signup')
def sign_up():
    """This function implements sign_up"""
    return render_template("signup.html")

@app.route('/signin/raiseissue')
def raise_issue():
    """This function implements """
    return render_template("raiseissue.html")


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)