from libs import controller
import web

urls = (
	"/msg", controller.msg,
    "/logout", controller.logout,
    "/signup", controller.signup,
	'/login', controller.login,
	'/api', controller.spi,
	'/msg', controller.main,
	'/id([0-9]+)', controller.profile,
	'/edit', controller.edit,
	'/around', controller.around,
	'/', controller.main,
    '/(.*)', controller.profile,
)