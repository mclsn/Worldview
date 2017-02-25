from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import json
import web

# Logged function
def logged():
    if web.config._session.login==1:
        return True
    else:
        return False

# DB Object to JSON
def dBJSON(IterBetterList):
	temp = []
	if not IterBetterList:
		return None
	for i in range(IterBetterList.__len__()):
		temp.append(json.dumps(IterBetterList.__getitem__(i)))
	return temp[0]

# JSON to Dict
def JSONtDict(IterBetterList):
	result = json.loads(IterBetterList)
	return result

def renderTemp(doc, jsonstr=None, sys=None):
	env = Environment(loader=FileSystemLoader('/home/projects/snw/views'), cache_size=0)
	template = env.get_template(str(doc))
	session = web.config._session
	try:
		return template.render(response=jsonstr, msg=sys, session=session)
	except TemplateNotFound:
		raise web.notfound()