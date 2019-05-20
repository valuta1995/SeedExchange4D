import datetime
import os
import time

print(os.environ['PYTHONPATH'].split(os.pathsep))

from se4d import Database

from bottle import template, Bottle, response, request, abort, run, static_file

DEFAULT_DB_FILE = "../db.sqlite"

BASE_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Ensure these variables include all the variables used in the application.
# Extra variables will not cause issues. missing variables will cause issues.
GLOBAL_APPLICATION_VARIABLES = [
    "provide_name", "provide_unit",
    "request_name", "request_unit",
    "transport_name",
    "caller_id", "caller_mode"
]

global_state = {"global_vars": GLOBAL_APPLICATION_VARIABLES}

server = Bottle()


@server.hook('after_request')
def hook_allow_cors():
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'


@server.get('/')
def get_empty():
    return "Please use <a href=\"./main_menu.vxml\">main_menu.vxml</a> instead." \
           "<br/>Alternatively call us through <a href=\"sip:9996151951@sip.lhr.aspect-cloud.net\">SIP</a>"


@server.get('/favicon.ico')
def abort_request():
    abort(404)


def get_user_data(caller_id):
    print("Stapling user data for %s to data package." % caller_id)

    conn = Database.create_connection(DEFAULT_DB_FILE)
    user = Database.select_user(conn, caller_id)
    if len(user) < 1 or len(user) > 1:
        return None
    user = user[0]
    trade_list = Database.select_offers(conn, user['id'])

    return {"user_data": {
        "trade_list": trade_list,
        "caller_id": caller_id,
    }}


@server.get('/<filename>.vxml')
def get_vxml_file(filename):
    filename = filename.replace(".", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    dic0 = dict()
    dic0.update(core_settings)
    dic0.update(global_state)
    dic0.update(seed_list)
    if 'caller_id' in request.query:
        data = get_user_data(request.query['caller_id'])
        if data is not None:
            dic0.update(data)
        else:
            print("User not found in system!")
    print(seed_list)
    instance = template("%s/templates/%s.tpl" % (BASE_PATH, filename), dic0)
    response.content_type = 'text/plain'
    return str(instance)


@server.get('/clips/<filename>.wav')
def get_vxml_file(filename):
    filename = filename.replace(".", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    response.content_type = 'audio/wav'
    return static_file("/%s.wav" % filename, root="%s/clips" % BASE_PATH)


@server.get('/static/<language>/<filename>.wav')
def get_vxml_file(language, filename):
    filename = filename.replace(".", "")
    filename = filename.replace("/", "")
    filename = filename.replace("\\", "")
    response.content_type = 'audio/wav'
    return static_file("/%s.wav" % filename, root="%s/static/%s" % (BASE_PATH, language))


def get_database_list(provide_name, provide_unit, request_name, request_unit, transport_name):
    # Here will be a request to show only entries that are available
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
        populate_dummy_db(provide_name, provide_unit, request_name, request_unit)
        return {"trade_list": dummy_db}


def populate_dummy_db(provide_name, provide_unit, request_name, request_unit):
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
    dic0.update(core_settings)
    dic0.update(global_state)
    dic0.update(seed_list)
    dic0.update(get_database_list(provide_name, provide_unit, request_name, request_unit, transport_name))
    instance = template("%s/templates/request_trade_list.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


def get_entry_from_db(db, trade_id):
    for entry in db:
        if entry['id'] == trade_id:
            return entry

    return None


def get_database_entry(trade_id):
    entry = get_entry_from_db(dummy_db, trade_id)
    if entry is None:
        print("We got a woot error over here.")
        abort(404)
    return {"trade_entry": entry}


@server.get('/trades/<trade_id:int>.vxml')
def get_single_trade(trade_id):
    trade_data = get_database_entry(trade_id)
    dic0 = dict()
    dic0.update(core_settings)
    dic0.update(global_state)
    dic0.update(seed_list)
    dic0.update(trade_data)
    instance = template("%s/templates/trade_entry.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


@server.get('/trades/delete/<trade_id:int>.vxml')
def delete_single_trade(trade_id):
    trade_data = get_database_entry(trade_id)
    # TODO check if trade entry has the same caller id and delete only in that case.
    dic0 = dict()
    dic0.update(core_settings)
    dic0.update(global_state)
    dic0.update(seed_list)
    dic0.update(trade_data)
    instance = template("%s/templates/offer_deleted.tpl" % BASE_PATH, dic0)
    response.content_type = 'text/plain'
    return str(instance)


@server.post('/trades/')
def post_new_trade():
    caller_id = request.forms.get("caller_id")
    provide_name = request.forms.get("provide_name")
    request_name = request.forms.get("request_name")

    print("%s wants %s and will give %s." % (caller_id, provide_name, request_name))

    audio_file = request.files.get("audio_name_location")
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    audio_file.save("%s/clips/%s_%s" % (BASE_PATH, timestamp, audio_file.filename), overwrite=True)

    return str("")


def initialize():
    global core_settings, seed_list

    # Set up the database if it does not yet exist
    conn = Database.create_connection(DEFAULT_DB_FILE)
    for statement in Database.DB_CREATE_TABLE:
        print(Database.execute_query(conn, statement))
    host = Database.get_setting_or_default(conn, "host", "localhost")
    print(host)
    port = Database.get_setting_or_default(conn, "port", "10123")
    print(port)
    public_host = Database.get_setting_or_default(conn, "public_host", "https://%s:%s/" % (host, port))
    core_settings = {
        # What version of VXML are you using
        "vxml_version": "2.1",
        "application": "/root.vxml",
    }
    seed_list = {"seed_list": [el[0] for el in Database.get_all_seeds(conn)]}

    conn.commit()

    return host, int(port)


def main():
    host, port = initialize()
    run(server, host=host, port=port)


main()
