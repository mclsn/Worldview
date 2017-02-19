from libs import controller
import web

urls = (
    '/.*', controller.signup,
)