import web
from libs import route, template
from libs import memcached

app = web.application(route.urls, globals()) 
session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'count': 0})

if __name__ == '__main__':
	app.run()
else:
	web.config.debug = False
	application = app.wsgifunc()