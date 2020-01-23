from flask import render_template, flash, redirect,url_for,request,session
from flask_login import login_required,logout_user,current_user,login_user,login_manager
from flask_wtf import FlaskForm
from wtforms import StringField, TextField, PasswordField, BooleanField, SubmitField,validators
from wtforms.validators import DataRequired
from ToDoApp import TDapp
from ToDoApp.forms import LoginForm,RegistrationForm,TaskForm,ModForm
from passlib.hash import sha256_crypt
import mysql.connector
import gc

def connection():
    conn = mysql.connector.connect(host="localhost",
                           user = "root",
                           passwd = "$$Shiva123",
                           db = "sample")
    c = conn.cursor()

    return c, conn


@TDapp.route('/')
@TDapp.route('/index')
def index():
    query="SELECT task,status,due_date FROM todolist;"
    cursor,cnx=connection()
    cursor.execute(query)
    posts=[list(result) for result in cursor]
    return render_template('index.html',posts=posts)

@TDapp.route('/add')
def addtask():
	form = TaskForm()
	if form.validate_on_submit():
		task=form.task.data
		due_date=form.due_date.data
		status=form.status.data
		query="INSERT INTO todolist VALUES(%s,%s,%s);"
		cursor,cnx=connection()
		cursor.execute(query,task,due_date,status)
		return redirect(url_for('index'))
	return render_template('addtask.html',title='Add task',form=form)

@TDapp.route('/modify')
def modifytask():
	form = ModForm()
	if form.validate_on_submit():
		task=form.task.data
		new_task=form.new_task.data
		due_date=form.due_date.data
		status=form.status.data
		cursor,cnx=connection()

		query="UPDATE todolist SET task=%s WHERE task=%s;"
		cursor.execute(query,new_task,task)
		
		query="UPDATE todolist SET due_date=%s WHERE task=%s;"
		cursor.execute(query,due_date,task)
		
		query="UPDATE todolist SET status=%s WHERE task=%s;"
		cursor.execute(query,status,task)
		return redirect(url_for('index'))

	return render_template('modifytask.html',title='Modify task',form =form)
'''
@TDapp.route('/Userjob/')
def userTDL():
	query="SELECT task,status,due_date FROM todolist;"
	cursor,cnx=connection()
	cursor.execute(query)
	posts=[list(result) for result in cursor]
	if username in session:
		return render_template('usertdl.html',username=username,posts=posts)
	else:
		return render_template('usertdl.html',posts=posts)
'''		

@TDapp.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if request.method== 'POST' and form.validate_on_submit():
		username=form.username.data
		password=form.password.data
		query="SELECT COUNT(*) FROM user WHERE username=%s AND password=%s;"
		cursor,cnx=connection()
		cursor.execute(query,username,password)
		
		#for post in cursor:
		#	if int(post)<=1:
		#		flash('Invalid username or password')
		#		return redirect(url_for('login'))
		#	else:
		session[username]=username
		return redirect(url_for('index'))
	return render_template('login.html', title='Sign In', form=form)

@TDapp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@TDapp.route('/register/', methods=["GET","POST"])
def register_page():
	try:
		form = RegistrationForm()

		if form.validate_on_submit():
			user_id=form.user_id.data
			name=form.name.data
			username  = form.username.data
			password = form.password.data

			c, conn = connection()

			c.execute("SELECT COUNT(*) FROM user WHERE user_id = '%s';",
			      (user_id))
			for x in c:
				if int(x[0]) > 0:
					flash("That user_id is already taken, please choose another")
					return render_template('register.html', form=form)

			c.execute("SELECT COUNT(*) FROM user WHERE username = '%s';",
			      (username))
			for x in c:
				if int(x[0]) > 0:
					flash("That username is already taken, please choose another")
					return render_template('register.html', form=form)

				else:
					c.execute("INSERT INTO user VALUES (%s, %s, %s, %s);",
					          (user_id,name,username,password))

					conn.commit()
					flash("Thanks for registering!")
					c.close()
					conn.close()
					gc.collect()

					session['logged_in'] = True
					session['username'] = username

					return redirect(url_for('index'))

		return render_template("register.html", form=form)

	except Exception as e:
		return(str(e))