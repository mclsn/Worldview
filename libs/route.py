from libs import controller
import web

urls = (
    "/logout", controller.logout,
    "/signup", controller.signup,
	'/login', controller.login,
	'/id([0-9]+)', controller.profile,
	'/edit', controller.edit,
	'/', controller.main,
    '/(.*)', controller.profile,
)