from flask import Flask, render_template, redirect, session, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, update
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
    return render_template("signup.html")

@app.route('/signin', methods=['GET', 'POST'])
def sign_in():
    """This function implements user/admin sign_in"""
    if request.method == 'POST':
        user = sessions.query(Users).filter_by(username =request.form['username'], password=request.form['password']).one()
        flash('You were successfully logged in')
        session['Username'] = request.form['username']
        session['id'] = user.id
        session['logged'] = True
        if user.designation == 'admin':
            return redirect(url_for('admin_view_issues'))
        else:
            return redirect(url_for('user_view_issues'))
        
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
        if designation == 'admin':
            admin = sessions.query(Users).filter_by(designation = 'admin', department = department)
            if admin != None:
                flash('Sorry there is an admin!!')
                return render_template("signup.html")
        newuser = Users(username=username, password=password, email=email, department=department, designation=designation)
        sessions.add(newuser)
        sessions.commit()
        flash('You were successfully signed up')
        return redirect(url_for('sign_in'))
    return render_template("signup.html")

@app.route('/signin/raiseissue', methods=['GET', 'POST'] )
def raise_issue():
    """This function implements raise_issues"""
    if 'Username' in session:
        username = session['Username'] 
        if request.method == 'POST':
            issuename = request.form['issuename']
            description = request.form['description']
            priority = request.form['priority']
            department = request.form['department']
            newissue = Issues(name=issuename, description=description, priority=priority, department=department, user_id = session['id'] )
            sessions.add(newissue)
            sessions.commit()
            flash('You have successfully raised an issue!')
            #return redirect(url_for('index'))
            return redirect(url_for('user_view_issues'))
        else:
            return render_template("raiseissue.html", user=username)
    else:
        return redirect(url_for('index'))

@app.route('/user/viewissues')
def user_view_issues():
    """This function implements view issues"""
    results = sessions.query(Issues).filter_by(user_id = session['id']).all()
    return render_template("allissues.html", results=results)

@app.route('/admin/viewissues')
def admin_view_issues():
    """This function implements view issues"""
    results = sessions.query(Issues).all()
    return render_template("allissues.html", results=results)



@app.route('/signout')
def sign_out():
    """This functions implements signout"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin/resolved', methods=['GET', 'POST'])
def resolve_issue():
    """This function implements view issues"""
    results = sessions.query(Issues).all()
    return render_template("allissues.html", results=results)

@app.route('/admin/update', methods=['POST'])
def update_issue():
    """This function implements update issues"""
    if request.method == 'POST':
        issue_id = request.form['issue_id']
        print(issue_id)
        issue_name = request.form['issue_name']
        status = request.form['status']
        assign_to = request.form['assign_to']

        #comment = request.form['comment']
        edit_issue = update(Issues).where(Issues.id==int(issue_id)).values(name=issue_name, assignned=assign_to, resolved=status)
        sessions.execute(edit_issue)
        sessions.commit()
        flash('You have successfully updated an issue!')


    return redirect(url_for("admin_view_issues"))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8080, debug=True)