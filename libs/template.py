from jinja2 import Environment, FileSystemLoader, TemplateNotFound
import os
import json
import web

# DB Object to JSON
def dBJSON(IterBetterList):
	temp = []
	for i in range(IterBetterList.__len__()):
		temp.append(json.dumps(IterBetterList.__getitem__(i)))
	return temp[0]

# JSON to Dict
def JSONtDict(IterBetterList):
	result = json.loads(IterBetterList)
	return result

def renderTemp(doc, jsonstr=None, errors=None):
	env = Environment(loader=FileSystemLoader('/home/projects/snw/views'))
	template = env.get_template(str(doc))
	try:
		return template.render(response=jsonstr, error=errors)
	except TemplateNotFound:
		raise web.notfound()