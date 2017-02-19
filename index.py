import web
from libs import route, template

#web.config.debug = True
wsgi_app = web.application(route.urls, globals()).wsgifunc()