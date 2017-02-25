import web
import itertools
import libs.template
import json
import datetime
import libs.utils

class Auth:

	db = web.database(dbn='postgres', db='db', user='postgres', pw='2339')

	def selectAll(self):
		result = self.db.query("""SELECT * FROM auth;""")
		result = self.db.select('auth')
		return result

	def checkValidateEmail(self, emailCheck):
		result = self.db.query("""SELECT * FROM auth WHERE data->>'email' = $email;""", vars={'email':emailCheck}).list()	
		return libs.template.dBJSON(result)

	def ckechUserBase(self, emailCheck, passwordCheck):
		result = self.db.query("""SELECT * FROM auth WHERE data->>'email' = $email;""", vars={'email':emailCheck}).list()
		try:
			result = libs.template.dBJSON(result)
			result = libs.template.JSONtDict(result)
			Utils =  libs.utils.utils()
			hPassword = Utils.HashKey(str(passwordCheck))
			if hPassword == result['data']['password']:
				return self.returnUserInfo(result['id'])
			else:
				return False
		except:
			return False

	def register(self, signupForm):
		Utils =  libs.utils.utils()
		hPassword = Utils.HashKey(str(signupForm.signupPassword))

		results = self.db.query("""
			INSERT INTO auth (data) VALUES ($authInfo);
			INSERT INTO users (data) VALUES ($mainData);
			""", 
			vars={
			"authInfo" : json.dumps({'email': str(signupForm.signupEmail), 'password' : str(hPassword)}),
			"mainData" : json.dumps({'fname': str(signupForm.signupFName), 'lname' : str(signupForm.signupLName)})
			})

		return results

	def returnUserInfo(self, userId):
		result = self.db.query("""SELECT * FROM users WHERE id = $IDu;""", vars={'IDu':userId}).list()
		try:
			return libs.template.JSONtDict(libs.template.dBJSON(result))
		except:
			return False