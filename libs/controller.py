import web
import json
import libs.template

class index:

	def GET(self):
		db = web.database(dbn='postgres', db='db', user='postgres', pw='2339')
		# userid = db.insert('users', username="A", password="B")
		users = db.select('users')
		web.setcookie('set', 'a', 3600)
		return libs.template.renderTemp('views/main.html', libs.template.dBJSON(users))
