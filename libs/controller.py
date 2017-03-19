# sudo pip install -I pillow

import web
import json
import libs.template, libs.models, libs.utils, libs.image
import urllib
import os
from urllib import parse

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

class edit:

	_valid = ['first_name', 'last_name', 'user_name']

	def GET(self):
		Utils = libs.utils.utils()
		session = web.config._session
		user_information = libs.models.Users().getUser(session.user_id)
		if(user_information):
			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				data = libs.template.renderTemp(doc = 'edit.html', jsonstr = user_information, csrf = Utils.csrf_token())
				return json.dumps([{'act' : 'add', 'data' : data, 'selector' : '#page'}])
			else:
				return libs.template.renderTemp(doc = 'edit.html', jsonstr = user_information, csrf = Utils.csrf_token(), extender="main.html")
		else:
			return libs.template.renderTemp(doc = '404.html')


	@csrf_protected
	def POST(self):
		Utils = libs.utils.utils()
		editData = web.input(_method='post')
		session = web.config._session
		fields = dict()

		_home = '/home/projects/snw'
		_path = lambda x: '/usr/av/' + x + '.jpg'
		_return = lambda attr,data,sel,typer='None': {'act' : attr, 'data' : data, 'selector' : sel, 'type' : typer}

		try:
			for key, value in editData.items():

				if (key == "user_avatar" and value != ""):
					import uuid
					Image = libs.image.image()

					unique_filename = str(uuid.uuid4())
					with open(_home + _path(unique_filename), "wb") as out_file:
						out_file.write(editData.user_avatar)

					if Image.CropProfile(_home + _path(unique_filename), 512):
						fields.update({'user_avatar' : unique_filename})

				elif (key == "user_name"):
					if not (libs.models.Edit().checkUsername(parse.unquote(value))):
						fields.update({key : parse.unquote(value)})

				elif (key in self._valid and value != ""):
					fields.update({key : parse.unquote(value)})

			if fields:
				user_setProperties = libs.models.Users().setProperty(session.user_id, fields)
			
			user_information = libs.models.Users().getUser(session.user_id)
			session.first_name = user_information['first_name']
			session.last_name = user_information['last_name']
			session.user_avatar = user_information['user_avatar']
			session.user_name = user_information['user_name']
			return json.dumps([ 
				_return('add', session.first_name + " " + session.last_name, '#headerName'),
				_return('attr', _path(session.user_avatar), '#headerAvatar', 'src'),
				_return('attr', _path(session.user_avatar), '#editPage_avatar', 'src'),
				_return('attr', Utils.csrf_token(), '#csrf', 'value'),
				_return('attr', '/logout?csrf=' + Utils.csrf_token(), '#head_LogoutLink', 'href')
				]) if (user_information) \
				else libs.template.renderTemp(doc = '404.html')

		except:
			user_information = libs.models.Users().getUser(session.user_id)
			return libs.template.renderTemp(doc = 'edit.html', jsonstr = user_information, csrf = Utils.csrf_token(), extender="main.html")

class profile:

	def GET(self, userID):
		Utils = libs.utils.utils()
		user_information = libs.models.Users().getUser(userID)
		if(user_information):
			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				data = libs.template.renderTemp(doc = 'profile.html', jsonstr = user_information, csrf = Utils.csrf_token())
				return json.dumps([{'act' : 'add', 'data' :data, 'selector' : '#page'}])
			else:
				return libs.template.renderTemp(doc = 'profile.html', jsonstr = user_information, csrf = Utils.csrf_token(), extender="main.html")
		else:
			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				data = libs.template.renderTemp(doc = '404.html')
				return json.dumps([{'act' : 'add', 'data' : data, 'selector' : '#scrollFix'}])
			else:
				return libs.template.renderTemp(doc = '404.html', extender="main.html")

	def POST(self):
		pass

class main:
	def GET(self):
		session = web.config._session
		Utils = libs.utils.utils()

		if(session.user_id != 0):
			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				data = libs.template.renderTemp(doc = 'im.html', csrf = Utils.csrf_token())
				return json.dumps([{'act' : 'add', 'data' : data, 'selector' : '#page'}])
			else:
				return libs.template.renderTemp(doc = 'im.html', csrf = Utils.csrf_token(), extender="main.html")
		else:
			return web.seeother('/login')

	def POST(self):
		pass

class signup:
	def GET(self):
		params = web.input(_method='get')
		Utils = libs.utils.utils()

		session = web.config._session
		msg = dict()
		data = ""
		if(session.user_id == 0):
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
					
			data = libs.template.renderTemp(
				doc = 'signup.html', 
				jsonstr = params, 
				sys = msg, 
				csrf = Utils.csrf_token()
			)

			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				return json.dumps([{'act' : 'add', 'data' : data, 'selector' : '#main_content', 'type' : 'add'}])
			else:
				return libs.template.renderTemp(doc = 'signup.html', csrf = Utils.csrf_token(), extender="main.html")

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
		if(session.user_id == 0):
			if(params.__contains__('c') == True):
				if(params.c == '1'):
					msg['text'] = "Wrong login or password"
					msg['status'] = 0

				elif(params.c == '2'):
					msg['text'] = "Successful registration"
					msg['status'] = 1
					
			data = libs.template.renderTemp(
					doc = 'login.html',
					jsonstr = params,
					sys = msg,
					csrf = Utils.csrf_token(),
				)

			if('HTTP_X_REQUESTED_WITH' in web.ctx.env and web.ctx.env['HTTP_X_REQUESTED_WITH'] == "XMLHttpRequest"):
				return json.dumps([{'act' : 'add', 'data' : data, 'selector' : '#main_content', 'type' : 'add'}])
			else:
				return libs.template.renderTemp(doc = 'login.html', csrf = Utils.csrf_token(), extender="main.html")

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
			for key, value in user_information.items():
				session[key] = value

			return web.seeother('/%s' % str(''))

		return web.seeother('/%s' % str('login?' + urllib.parse.urlencode(fields)))

class logout:
	@csrf_protected
	def POST(self):
		session = web.config._session
		if(session.user_id != 0):
			session.kill()
			return json.dumps([{'act' : 'reload'}])
		return libs.template.renderTemp('404.html')