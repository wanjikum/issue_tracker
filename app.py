from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_setup import Base, Issues, Users

app = Flask(__name__)
app.secret_key = "jijikiki"


engine = create_engine('sqlite:///issue_tracker.db')

Base.metadata.create_all(engine)
DBSession =  sessionmaker(bind=engine)
sessions = DBSession()

@app.route('/')
def index():
    """This function implements sign_in"""
    return render_template("index.html")

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    """This function implements user/admin sign_in"""
    if request.method == 'POST':
        user = sessions.query(Users).filter_by(username =request.form['username'], password=request.form['password']).one()
        return redirect(url_for('raise_issue'))
    return render_template("signin.html")

@app.route('/signup', methods=['GET', 'POST'] )
def sign_up():
    """This function implements user/admin sign_up"""
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        department = request.form['department']
        designation = request.form['usertype']
        newuser = Users(username=username, password=password, email=email, department=department, designation=designation)
        sessions.add(newuser)
        sessions.commit()
        return redirect(url_for('index'))
    return render_template("signup.html")

@app.route('/signin/raiseissue', methods=['GET', 'POST'] )
def raise_issue():
    """This function implements raise_issues"""
    if request.method == 'POST':
        issuename = request.form['issuename']
        description = request.form['description']
        priority = request.form['priority']
        department = request.form['department']
        newissue = Issues(name=issuename, description=description, priority=priority, department=department)
        sessions.add(newissue)
        sessions.commit()
        #return redirect(url_for('index'))
    return render_template("raiseissue.html")

@app.route('/signin/signout')
def sign_out():
    """This functions implements signout"""
    return redirect(url_for('index'))


if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=True)