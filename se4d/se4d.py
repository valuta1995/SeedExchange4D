import os

from bottle import template, Bottle, response, request, abort, run

HOST_NAME = "https://vxml.valutadev.com"

CORE_SETTINGS = {
    "vxml_version": "2.1",
    "application": "%s/root.vxml" % HOST_NAME,
}

BASE_PATH = os.getcwd()[:-4]

global_state = dict()
global_state.update({"global_vars": ["lang", "user", "product", "quantity", "price", "duration", "path", "ext"]})

server = Bottle()


@server.hook('after_request')
def hook_allow_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@server.get('/')
def get_empty():
    return "Please use <a href=\"./root.vxml\">root.vxml</a> instead."


@server.get('/favicon.ico')
def abort_request():
    abort(404)


@server.get('/<filename>.vxml')
def get_vxml_file(filename):
    dic0 = dict()
    dic0.update(CORE_SETTINGS)
    dic0.update(global_state)
    instance = template("%stemplates//%s.tpl" % (BASE_PATH, filename), dic0)
    response.content_type = 'text/plain'
    return str(instance)


run(server, host="localhost", port=10123)
