import web
import json
import libs.template, libs.models
import urllib

class main:
	def GET(self):
		session = web.config._session
		if(session.login == 0):
			return libs.template.renderTemp('main.html')
		else:
			return libs.template.renderTemp('main.html')

	def POST(self):
		pass

class signup:
	def GET(self):
		params = web.input(_method='get')
		session = web.config._session
		msg = dict()
		if(session.login == 0):
			if(params.__contains__('c') == True):
				if(params.c == '1'):
					msg['text'] = "Please, fill out all filds"
					msg['status'] = 0
				elif(params.c == '2'):
					msg['text'] = "This email address is already in use"
					msg['status'] = 0
				elif(params.c == '3'):
					msg['text'] = "Something went wrong..."
					msg['status'] = 0
				return libs.template.renderTemp('signup.html', params, msg)
			return libs.template.renderTemp('signup.html')
		else:
			return web.seeother('/')

	def POST(self):
		signupData = web.input(_method='post')
		email = signupData.signupEmail
		fname = signupData.signupFName
		lname = signupData.signupLName

		fields = {'c' : 2}
		Fail = False;

		for key, value in signupData.items():
			if value == "":
				Fail = True
			elif key != "signupPassword":
				fields.update({key : value})

		if Fail:
			fields['c'] = 1
			return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

		# Search in database
		auth = libs.models.Auth()
		if(auth.checkValidateEmail(str(signupData.signupEmail)) == None):
			if(auth.register(signupData)):
				return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))
			else:
				fields['c'] = 3
				return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

		return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

class login:
	def GET(self):
		params = web.input(_method='get')
		session = web.config._session
		msg = dict()
		if(session.login == 0):
			if(params.__contains__('c') == True):
				if(params.c == '1'):
					msg['text'] = "Wrong login or password"
					msg['status'] = 0
					return libs.template.renderTemp('login.html', params, msg)
				elif(params.c == '2'):
					msg['text'] = "Successful registration"
					msg['status'] = 1
				return libs.template.renderTemp('login.html', params, msg)
			return libs.template.renderTemp('login.html')
		else:
			return web.found(web.ctx.env.get(u'HTTP_REFERER', u'/'))

	def POST(self):
		loginData = web.input(_method='post')
		email = loginData.email
		password = loginData.password

		fields = dict()
		Fail = False;

		for key, value in loginData.items():
			if value == "":
				Fail = True
			elif key != "password":
				fields.update({key : value})

		fields.update({'c' : 1})
		if Fail:
			return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))

		auth = libs.models.Auth()
		if(auth.ckechUserBase(str(loginData.email), str(loginData.password)) == True):
			session = web.config._session
			session.login = 1
			return web.seeother('/%s' % str(''))


		return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))

class logout:
	def GET(self):
		session = web.config._session
		if(session.login == 1):
			session.kill()
			web.seeother('/')
		return libs.template.renderTemp('404.html')