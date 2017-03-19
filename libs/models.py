import web
import itertools
import libs.template
import json
import datetime
import libs.utils
from neo4j.v1 import GraphDatabase, basic_auth

class Edit:
	driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "Mun152339"))
	session = driver.session()	

	def checkUsername(self, user_name):
		result = self.session.run("MATCH (a:Person) WHERE a.user_name = {user_name} "
		           "RETURN properties(a)", {"user_name": str(user_name)})

		for i in result:
			return i[0]

class Users:
	driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "Mun152339"))
	session = driver.session()

	def insertOnce(self, userId, dataPart):
		self.session.run("CREATE (a:Person {first_name: {first_name}, last_name: {last_name}, user_id: {user_id}})",
			{"first_name": str(dataPart.signupFName), "last_name": str(dataPart.signupLName), "user_id": str(userId)})
		return True

	def getUser(self, userId):
		result = False;
		if(str(userId).isdigit()):
			result = self.session.run("MATCH (a:Person) WHERE a.user_id = {userId} "
		           "RETURN properties(a)", {"userId": str(userId)})
		else:
			result = self.session.run("MATCH (a:Person) WHERE a.user_name = {userId} "
		           "RETURN properties(a)", {"userId": str(userId)})

		user_information = False
		for i in result:
			user_information = i[0]			
		return user_information

	def setProperty(self, userId, jsonSet):
		result = self.session.run("MATCH (user:Person) WHERE user.user_id = {userId} "
		           "SET user += {jsonSet}", {"userId": str(userId), "jsonSet": jsonSet})
		if(result): 
			return True
		else:
			return False

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
				return result['id']
			else:
				return False
		except:
			return False

	def register(self, signupForm):
		Utils =  libs.utils.utils()
		hPassword = Utils.HashKey(str(signupForm.signupPassword))

		results = self.db.query("""INSERT INTO auth (data) VALUES ($authInfo); SELECT currval('auth_id_seq');""", 
			vars={"authInfo" : json.dumps({'email': str(signupForm.signupEmail), 'password' : str(hPassword)})})[0]

		return results.currval

	def returnUserInfo(self, userId):
		result = self.db.query("""SELECT * FROM users WHERE id = $IDu;""", vars={'IDu':userId}).list()
		try:
			return libs.template.JSONtDict(libs.template.dBJSON(result))
		except:
			return False