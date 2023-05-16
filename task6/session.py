import db
import os
from http import cookies

def get_or_create_session_id(user_id):
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    if session_id is None:
        session_id = db.create_session()
        cookies_object = cookies.SimpleCookie()
        cookies_object["session_id"] = session_id
        print (cookies_object.output()) #upisivanje cookie-a u header
    return session_id

def add_to_session(params):
    session_id = get_or_create_session_id()
    _, data = db.get_session(session_id)#vracanje do sada odabranih podataka
    for id in params.keys():
        data[id] = params.getvalue(id)
    db.replace_session(session_id, data)

def get_session_data():
    session_id = get_or_create_session_id()
    _, data = db.get_session(session_id)
    return data

def logout():
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    if session_id is not None:
        db.delete_session(session_id)
        cookies_object = cookies.SimpleCookie()
        cookies_object["session_id"] = ""
        cookies_object["session_id"]["expires"] = 'Thu, 01 Jan 1970 00:00:00 GMT'
        print(cookies_object.output())