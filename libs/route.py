from libs import controller
import web

urls = (
    "/logout", controller.logout,
    "/signup", controller.signup,
	'/login', controller.login,
    '/.*', controller.main,
)