from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def sign_in():
    """This function implements sign_in"""
    return render_template("signin.html")

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080)