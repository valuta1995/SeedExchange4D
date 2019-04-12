import datetime
import os
import time

from bottle import template, Bottle, response, request, abort, run, static_file

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
    "transport_name",
    "caller_id"
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
dummy_db = []
server = Bottle()


@server.hook('after_request')
def hook_allow_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@server.get('/')
def get_empty():
    return "Please use <a href=\"./root.vxml\">root.vxml</a> instead." \
           "<br/>Alternatively call us through <a href=\"sip:9996151951@sip.lhr.aspect-cloud.net\">SIP</a>"


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


@server.get('/clips/<filename>.wav')
def get_vxml_file(filename):
    filename = filename.replace(".", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    response.content_type = 'audio/wav'
    return static_file("%s.wav" % filename, root="%sclips/" % BASE_PATH)


def get_database_list(provide_name, provide_unit, request_name, request_unit, transport_name):
    # Here will be a request to show only entries that are available
    global dummy_db
    if transport_name == 'false':
        dummy_db = [
            {"id": 1234, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1236, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1238, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},
        ]
        return {"trade_list": dummy_db}
    else:
        dummy_db = [
            {"id": 1234, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1235, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "false",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1236, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1237, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "false",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},

            {"id": 1238, "provide_name": request_name, "provide_unit": request_unit, "request_name": provide_name,
             "request_unit": provide_unit, "transport_name": "true",
             "audio_name_location": "20190412_181710_audio_name_location-1555093030557.wav"},
        ]
        return {"trade_list": dummy_db}


@server.post('/search_trade/')
def post_search_trade():
    caller_id = request.forms.get("caller_id")
    transport_name = request.forms.get("transport_name")

    provide_name = request.forms.get("provide_name")
    provide_unit = request.forms.get("provide_unit")

    request_name = request.forms.get("request_name")
    request_unit = request.forms.get("request_unit")

    print("%s wants %s of %s and will give %s of %s. Transport %s." % (
        caller_id, provide_unit, provide_name, request_unit, request_name, transport_name
    ))

    dic0 = dict()
    dic0.update(CORE_SETTINGS)
    dic0.update(global_state)
    dic0.update(seed_list)
    dic0.update(get_database_list(provide_name, provide_unit, request_name, request_unit, transport_name))
    instance = template("%stemplates//request_trade_list.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


def get_entry_from_db(db, trade_id):
    for entry in db:
        if entry['id'] == trade_id:
            return entry

    return None


def get_database_entry(trade_id):
    global dummy_db
    entry = get_entry_from_db(dummy_db, trade_id)
    if entry is None:
        print("We got a woot error over here.")
        abort(404)
    return {"trade_entry": entry}


@server.get('/trades/<trade_id:int>.vxml')
def get_single_trade(trade_id):
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
def post_new_trade():
    provide_name = request.forms.get("provide_name")
    provide_unit = request.forms.get("provide_unit")
    print("Want %s of %s." % (provide_unit, provide_name))

    request_name = request.forms.get("request_name")
    request_unit = request.forms.get("request_unit")
    print("Give %s of %s." % (request_unit, request_name))

    transport_name = request.forms.get("transport_name")
    print("Transport by %s." % transport_name)

    audio_file = request.files.get("audio_name_location")
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    audio_file.save("%sclips/%s_%s" % (BASE_PATH, timestamp, audio_file.filename), overwrite=True)

    return str("")


run(server, host="localhost", port=10123)
