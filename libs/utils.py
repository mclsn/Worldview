import hashlib
import web

class utils:
	_SK = 'x5ap[40wl2]a#g?'

	def HashKey(self, password):
		hPass = hashlib.md5(password.encode('utf-8'))
		return hPass.hexdigest()

	def csrf_token(self):
		session = web.config._session
		if 'csrf' not in session:
			from uuid import uuid4
			session.csrf=uuid4().hex
		return session.csrf