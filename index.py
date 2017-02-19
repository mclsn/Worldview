import web
from libs import route, template

def notfound():
	return web.notfound("404. Not found")

#web.config.debug = True
wsgi_app = web.application(route.urls, globals()).wsgifunc()