import web
import json
import libs.template, libs.models

class main:
	def GET(self):
		session = web.config._session
		if(session.login == 0):
			return web.seeother('/login')
		else:
			return libs.template.renderTemp('main.html')

	def POST(self):
		pass

class signup:
	def GET(self):
		session = web.config._session
		if(session.login == 0):
			return libs.template.renderTemp('signup.html')
		else:
			return web.seeother('/')

	def POST(self):
		signupData = web.input(_method='post')

		# Check empty values
		for key, value in signupData.items():
			if value == "":
				error = "Please, fill out all filds"
				return libs.template.renderTemp('signup.html', signupData, error)

		# Search in database
		auth = libs.models.Auth()
		if(auth.checkValidateEmail(str(signupData.signupEmail)) == None):
			if(auth.register(signupData)):
				return web.seeother('/%s' % str('login?e=2'))

		error = "Wrong login or password"
		return libs.template.renderTemp('signup.html', signupData, error)

class login:
	def GET(self):
		params = web.input(_method='get')
		session = web.config._session
		if(session.login == 0):
			if(params.__contains__('e') == True):
				if(params.e == '1'):
					error = "Wrong login or password"
					return libs.template.renderTemp('login.html', params, error)
				elif(params.e == '2'):
					error = "Successful registration"
					return libs.template.renderTemp('login.html', params, error)
			return libs.template.renderTemp('login.html')
		else:
			return web.found(web.ctx.env.get(u'HTTP_REFERER', u'/'))

	def POST(self):
		loginForm = web.input(_method='post')
		email = loginForm.loginEmail
		password = loginForm.loginPassword

		#check empty values
		if email != "" and password == "":
			return web.seeother('/%s' % str('login?e=1&email=' + email))
		elif email == "" or password == "":
			return web.seeother('/%s' % str('login?e=1'))
		else:
			auth = libs.models.Auth()
			if(auth.ckechUserBase(str(loginForm.loginEmail), str(loginForm.loginPassword)) == True):
				session = web.config._session
				session.login = 1
				return web.seeother('/%s' % str(''))
		return web.seeother('/%s' % str('login?e=1&email=' + email))

class logout:
	def GET(self):
		session = web.config._session
		if(session.login == 1):
			session.kill()
			web.seeother('/login')
		return libs.template.renderTemp('404.html')