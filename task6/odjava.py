#!python.exe
import db
import session
session_id=session.get_or_create_session_id()
db.delete_session(session_id)