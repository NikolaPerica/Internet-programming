#!python.exe

import db 
import password_utils
import session

def register(username, email, password):
    user_id = db.create_user(username, email, password)
    if user_id:
        return True
    else:
        return False

def check_email(email):
    all_users=db.get_users()
    for user in all_users:
        if email in user:
            return True
    return False

def check_username(username):
    all_users=db.get_users()
    for user in all_users:
        if username in user:
            return True
    return False
        
def authenticate(username, password):
    users = db.get_users()
    user1=None
    for user in users:
        if username in user:
            user1=user
    if (user1 and password_utils.verify_password(password, user1[3])):
        return True, user1[0]
    else:
        return False, None

