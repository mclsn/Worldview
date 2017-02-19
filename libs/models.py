import web
import itertools
import libs.template
import json

class Auth:
	db = web.database(dbn='postgres', db='db', user='postgres', pw='2339')

	def selectAll(self):
		result = self.db.query("""SELECT * FROM auth;""")
		result = self.db.select('auth')
		return result

	def checkValidateEmail(self, emailCheck):
		result = self.db.query("""SELECT * FROM auth WHERE data->>'email' = $email;""", vars={'email':emailCheck}).list()	
		return libs.template.dBJSON(result)

	def register(self, emailAuth, passwordAuth):
		results = self.db.query("""INSERT INTO auth (data) VALUES ($e);""", vars={"e" : json.dumps({'email': str(emailAuth), 'password' : str(passwordAuth)})})
		return results