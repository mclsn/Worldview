import web
import memcache

class MemCacheStore(web.session.Store):
    mc = None
    def __init__(self):
        self.mc = memcache.Client(['127.0.0.1:11211'], debug=0)
    def __contains__(self, key):
        return self.mc.get(key) != None
    def __getitem__(self, key):
        return self.mc.get(key)
    def __setitem__(self, key, value):
        self.mc.set(key, value, time = web.config.session_parameters["timeout"])
    def __delitem__(self, key):
        self.mc.delete(key)
    def cleanup(self, timeout):
        pass # Not needed as we assigned the timeout to memcache