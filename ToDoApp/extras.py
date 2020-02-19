
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

 <!--<a href="{{url_for('login')}}">Login</a>
        <a href="{{url_for('register_page')}}">Register</a>
        <a href="{{url_for('logout')}}">Logout</a>-->