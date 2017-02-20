from libs import controller
import web

urls = (
	"/count", controller.count,
    "/reset", controller.reset,
	'/login', controller.login,
    '/.*', controller.signup,
)