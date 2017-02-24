import hashlib

class utils:
	_SK = 'x5ap[40wl2]a#g?'

	def Hash(self, password):
		hPass = hashlib.md5(password.encode('utf-8'))
		return hPass.hexdigest()