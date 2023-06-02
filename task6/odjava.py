#!python.exe
import db
import session
session_id=session.get_or_create_session_id
db.destroy_session(session_id)