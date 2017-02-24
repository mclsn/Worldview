import web
from libs import route, template
from libs import memcached

app = web.application(route.urls, globals())
store = memcached.MemCacheStore()
web.config.session_parameters['cookie_name'] = 'wvid'
web.config.session_parameters['max_age'] = (60 * 60 * 24) * 365
session = web.session.Session(app, store, initializer={'login': 0, 'privilage': 0})
web.config._session = session

if __name__ == '__main__':
	app.run()
else:
	web.config.debug = False
	application = app.wsgifunc()