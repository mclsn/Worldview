import web

class Api:

	def addFriend(self, selfID, targetID):
		try:
			if(selfID != targetID and str(selfID).isdigit() and str(targetID).isdigit()):
				import libs.models
				action = libs.models.Users().addFriend(selfID, targetID)
				if(action):
					return True
		except:
			return False
		else:
			return False

	def delFriend(self, selfID, targetID):
		try:
			if(selfID != targetID and str(selfID).isdigit() and str(targetID).isdigit()):
				import libs.models
				action = libs.models.Users().delFriend(selfID, targetID)
				if(action):
					return True
		except:
			return False
		else:
			return False

	def editProfile(self, selfProperties, Data):
		_valid 	= ['first_name', 'last_name', 'user_name']
		_home = '/home/projects/snw'
		_path = lambda x: '/usr/av/' + x + '.jpg'

		from datetime import datetime
		from urllib import parse
		import libs.models
		import libs.image
		import libs.template

		Utils = libs.utils.utils()
		fields = dict()

		try:
			if('user_birth_year' in Data):
				year = Data['user_birth_year'];
				month = Data['user_birth_month'];
				day = Data['user_birth_day'];
				fields.update({'user_birthday' : '{:%Y-%m-%d}'.format(datetime(int(year), int(month), int(day)))})

			for key, value in Data.items():

				if (key == "user_avatar" and value != ""):
					import uuid
					Image = libs.image.image()

					unique_filename = str(uuid.uuid4())
					with open(_home + _path(unique_filename), "wb") as out_file:
						out_file.write(Data.user_avatar)

					if Image.CropProfile(_home + _path(unique_filename), 512):
						fields.update({'user_avatar' : unique_filename})

				elif (key == "user_name"):
					if not (libs.models.Edit().checkUsername(parse.unquote(value))):
						fields.update({key : parse.unquote(value)})

				elif (key in _valid and value != ""):
					fields.update({key : parse.unquote(value)})

			if fields:
				user_setProperties = libs.models.Users().setProperty(selfProperties.user_id, fields)
				if user_setProperties:
					return True
		except:
			return False
		else:
			return False