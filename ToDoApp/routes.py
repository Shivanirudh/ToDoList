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
@TDapp.route('/index',methods=['GET', 'POST'])
def index():
    query="SELECT task,status,due_date FROM todolist;"
    cursor,cnx=connection()
    cursor.execute(query)
    posts=[list(result) for result in cursor]
    return render_template('index.html',posts=posts)

@TDapp.route('/add',methods=['GET', 'POST'])
def addtask():
	form = TaskForm()
	if form.validate_on_submit() and request.method=='POST':
		task=form.task.data
		due_date=form.due_date.data
		status=form.status.data
		query=("INSERT INTO todolist VALUES(%s,%s,%s);")
		cursor,cnx=connection()
		data_query=(task,due_date,status)
		cursor.execute(query,data_query)
		return redirect(url_for('index'))
	return render_template('addtask.html',title='Add task',form=form)

@TDapp.route('/modify',methods=['GET', 'POST'])
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
