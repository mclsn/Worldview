import web
import json
import libs.template, libs.models

class count:
	def GET(self):
		if web.config.get('_session') is None:
			session = web.session.Session(app, web.session.DiskStore('sessions'), {'count': 0})
			session.count = 0
			web.config._session = session
			return session
		else:
			session = web.config._session
			if 'count' in session:
				session.count += 1
			else:
				session.count = 0
			return session.count

class reset:
	def GET(self):
		session = web.config._session
		session.kill()
		return ""

class signup:
	def GET(self):
		#db = web.database(dbn='postgres', db='db', user='postgres', pw='2339')
		# userid = db.insert('users', username="A", password="B")
		#users = db.select('auth')
		#web.setcookie('set', 'a', 3600)
		return libs.template.renderTemp('signup.html')

	def POST(self):
		post_input = web.input(_method='post')

		# Check empty values
		for key, value in post_input.items():
			if value == "":
				error = "Please, fill out all filds"
				return libs.template.renderTemp('signup.html', post_input, error)

		# Search in database
		auth = libs.models.Auth()
		if(auth.checkValidateEmail(str(post_input.signupEmail)) == None):
			if(auth.register(post_input.signupEmail, post_input.signupPassword)):
				return True

		return False

class login:
	def GET(self):
		return libs.template.renderTemp('login.html')

	def POST(self):
		loginForm = web.input(_method='post')

		#check empty values
		for key, value in loginForm.items():
			if value == "":
				error = "Please, fill out all filds"
				return libs.template.renderTemp('input.html', post_input, error)

		return False
