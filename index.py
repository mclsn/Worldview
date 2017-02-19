import web
from libs import route

wsgi_app = web.application(route.urls, globals()).wsgifunc()