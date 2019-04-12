import os

from bottle import template, Bottle, response, request, abort, run

# Where is the application root hosted?
HOST_NAME = "https://vxml.valutadev.com"

# Some global settings
CORE_SETTINGS = {
    # What version of VXML are you using
    "vxml_version": "2.1",
    "application": "%s/root.vxml" % HOST_NAME,
}

BASE_PATH = os.getcwd()[:-4]

# Ensure these variables include all the variables used in the application.
# Extra variables will not cause issues. missing variables will cause issues.
GLOBAL_APPLICATION_VARIABLES = [
    "provide_name", "provide_unit",
    "request_name", "request_unit",
    "transport_name"
]

LIST_OF_SUPPORTED_SEEDS = [
    {"name": "yam", "unit": "bags"},
    {"name": "soybeans", "unit": "bags"},
    {"name": "maize", "unit": "bags"},
    {"name": "rice", "unit": "bags"},
    {"name": "wheat", "unit": "bags"},
]

global_state = {"global_vars": GLOBAL_APPLICATION_VARIABLES}
seed_list = {"seed_list": LIST_OF_SUPPORTED_SEEDS}
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
    filename = filename.replace(".", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    dic0 = dict()
    dic0.update(CORE_SETTINGS)
    dic0.update(global_state)
    dic0.update(seed_list)
    instance = template("%stemplates//%s.tpl" % (BASE_PATH, filename), dic0)
    response.content_type = 'text/plain'
    return str(instance)


@server.post('/search_trade')
def get_vxml_file():
    print(request)
    dic0 = dict()
    dic0.update(CORE_SETTINGS)
    dic0.update(global_state)
    dic0.update(seed_list)
    instance = template("%stemplates//request_trade_list.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


def get_database_entry(trade_id):
    return {"trade_data": {
        "provide_name": "rice",
        "request_name": "wheat",
        "transport_name": "deliver",
        "audio_name_location": "John Doe %d from Amsterdam" % trade_id
    }}


@server.get('/trades/<trade_id:int>.vxml')
def get_vxml_file(trade_id):
    trade_data = get_database_entry(trade_id)
    dic0 = dict()
    dic0.update(CORE_SETTINGS)
    dic0.update(global_state)
    dic0.update(seed_list)
    dic0.update(trade_data)
    instance = template("%stemplates//trade_entry.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


@server.post('/trades/')
def get_vxml_file():
    body = request.body.read()
    print(body)
    # trade_data = get_database_entry(trade_id)
    # dic0 = dict()
    # dic0.update(CORE_SETTINGS)
    # dic0.update(global_state)
    # dic0.update(seed_list)
    # dic0.update(trade_data)
    # instance = template("%stemplates//trade_entry.tpl" % BASE_PATH, dic0)
    # response.content_type = 'text/plain'
    return str("")


run(server, host="localhost", port=10123)
