import web
import json
import libs.template, libs.models, libs.utils
import urllib


def csrf_protected(f):
	def decorated(*args,**kwargs):
		session = web.config._session
		inp = web.input()
		if not ('csrf' in inp and inp.csrf == session.pop('csrf',None)):
			raise web.HTTPError(
				"400 Bad request",
				{'content-type':'text/html'},
				inp.items())
		return f(*args,**kwargs)
	return decorated

class main:
	def GET(self):
		session = web.config._session
		Utils = libs.utils.utils()
		if(session.login == 0):
			return libs.template.renderTemp(
				doc = 'main.html', 
				csrf = Utils.csrf_token()
			)
		else:
			return libs.template.renderTemp(
				doc = 'main.html', 
				csrf = Utils.csrf_token()
			)

	def POST(self):
		pass

class signup:
	def GET(self):
		params = web.input(_method='get')
		Utils = libs.utils.utils()

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
				return libs.template.renderTemp(
					doc = 'signup.html', 
					jsonstr = params, 
					sys = msg, 
					csrf = Utils.csrf_token()
				)

			return libs.template.renderTemp(
				doc = 'signup.html', 
				csrf = Utils.csrf_token()
			)	
		else:
			return web.seeother('/')

	@csrf_protected
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
			elif key != "signupPassword" and key != "csrf":
				fields.update({key : value})

		if Fail:
			fields['c'] = 1
			return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

		# Search in database
		if(libs.models.Auth().checkValidateEmail(str(signupData.signupEmail)) == None):
			userGetId = libs.models.Auth().register(signupData)
			if(userGetId):
				libs.models.Users().insertOnce(userGetId, signupData)
				return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))
			else:
				fields['c'] = 3
				return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

		return web.seeother('/%s' % str('signup?' + urllib.parse.urlencode(fields)))

class login:
	def GET(self):
		params = web.input(_method='get')
		session = web.config._session
		Utils = libs.utils.utils()

		msg = dict()
		if(session.login == 0):
			if(params.__contains__('c') == True):
				if(params.c == '1'):
					msg['text'] = "Wrong login or password"
					msg['status'] = 0

				elif(params.c == '2'):
					msg['text'] = "Successful registration"
					msg['status'] = 1

				return libs.template.renderTemp(
					doc = 'login.html',
					jsonstr = params,
					sys = msg,
					csrf = Utils.csrf_token()
				)

			return libs.template.renderTemp(
				doc = 'login.html',
				csrf = Utils.csrf_token()
			)
		else:
			return web.found(web.ctx.env.get(u'HTTP_REFERER', u'/'))

	@csrf_protected
	def POST(self):
		loginData = web.input(_method='post')
		email = loginData.email
		password = loginData.password

		fields = dict()
		Fail = False;

		for key, value in loginData.items():
			if value == "":
				Fail = True
			elif key != "password" and key != "csrf":
				fields.update({key : value})

		fields.update({'c' : 1})
		if Fail:
			return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))

		user = libs.models.Auth().ckechUserBase(str(loginData.email), str(loginData.password))
		if(user):
			user_information = libs.models.Users().getUser(user)

			session = web.config._session
			session.login = user_information['user_id']
			session.fname = user_information['first_name']
			session.lname = user_information['last_name']
			return web.seeother('/%s' % str(''))


		return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))

class logout:
	def GET(self):
		session = web.config._session
		if(session.login != 0):
			session.kill()
			web.seeother('/')
		return libs.template.renderTemp('404.html')