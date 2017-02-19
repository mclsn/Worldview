import web

class Auth:
	db = web.database(dbn='postgres', db='db', user='postgres', pw='2339')

	def selectAll(self):
		result = db.select('auth')
		return result

	def countUsers(self, usernameCheck):
		result = db.query("SELECT COUNT(*) AS id FROM auth")
		return result