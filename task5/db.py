import mysql.connector # "C:\ProgramData\Anaconda3\python.exe" -m pip install mysql-connector 
import json
import password_utils
import os
from http import cookies

db_conf = {
    "host":"localhost",
    "db_name": "np",
    "user":"root",
    "passwd":""
}

def get_DB_connection():
    mydb = mysql.connector.connect(
        host=db_conf["host"],
        user=db_conf["user"],
        passwd=db_conf["passwd"],
        database=db_conf["db_name"]
    )
    return mydb

def create_session(user_id):
    query = "INSERT INTO sessions (session_id, data) VALUES (%s, %s)"
    values = (user_id, json.dumps({}))
    mydb = get_DB_connection()
    cursor = mydb.cursor(buffered=True)
    cursor.execute(query, values)
    mydb.commit()
    return cursor.lastrowid

def get_or_create_session_id(user_id):
    http_cookies_str = os.environ.get('HTTP_COOKIE', '')
    get_all_cookies_object = cookies.SimpleCookie(http_cookies_str)
    session_id = get_all_cookies_object.get("session_id").value if get_all_cookies_object.get("session_id") else None
    if session_id is None:
        session_id = create_session(user_id)
        cookies_object = cookies.SimpleCookie()
        cookies_object["session_id"] = session_id
        print (cookies_object.output()) #upisivanje cookie-a u header
    return session_id

def delete_session(session_id):
    query = "DELETE FROM sessions WHERE session_id = %s"
    values = (session_id,)
    mydb = get_DB_connection()
    cursor = mydb.cursor(buffered=True)
    cursor.execute(query, values)
    mydb.commit()


def get_data(mydb,session_id):
    cursor = mydb.cursor(buffered=True)
    query = "SELECT data FROM sessions WHERE session_id= %s"
    values = (session_id,)
    cursor.execute(query, values)
    session_data = cursor.fetchone()
    session_dict = json.loads(session_data[0])
    return session_dict

def get_session(session_id):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM sessions WHERE session_id=" + str(session_id))
    myresult = cursor.fetchone()
    return myresult[0], json.loads(myresult[1])

def replace_session(session_id, data):#replace-prvo izbrisi, a onda ubaci (delete/insert)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("""
    REPLACE INTO sessions(session_id,data) 
    VALUES (%s,%s)""",
    (session_id, json.dumps(data)))
    mydb.commit()

def add_to_session(params, session_id):
    _, data = get_session(session_id)#vracanje do sada odabranih podataka
    for article_id in params.keys():
        data[article_id] = params[article_id].value
    replace_session(session_id, data)

def change_password(session_id, new_password):
    mydb = get_DB_connection()
    cursor = mydb.cursor(buffered=True)
    hashed_password =password_utils.hash_password(new_password)
    query = "UPDATE users SET password = %s WHERE id = %s"
    values = (hashed_password, session_id)
    cursor.execute(query, values)
    mydb.commit()


def create_user(ime, email, password):
    query = "INSERT INTO users (ime, email, password) VALUES (%s, %s, %s)"
    hashed_password=password_utils.hash_password(password)
    values = (ime, email, hashed_password)
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute(query, values)
    mydb.commit()
    return cursor.lastrowid 

def get_user_by_username(ime):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE ime=%s"
    val = (str(ime), )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    return user

def get_name(session_id):
    mydb = get_DB_connection()
    cursor = mydb.cursor(buffered=True)
    query = "SELECT ime FROM users WHERE id= %s"
    values = (session_id,)
    cursor.execute(query, values)
    user_name = cursor.fetchone()[0]
    return user_name

def get_users():
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    return myresult

def get_user(email, password):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    sql = "SELECT * FROM users WHERE email=%s"
    val = (email, )
    cursor.execute(sql, val)
    user = cursor.fetchone()
    cursor.close()
    mydb.close()
    if user != None:
        stored_password_hash = user[3]
        if password_utils.verify_password(password, stored_password_hash):
            return True
    return False

def get_user_id(email):
    mydb = get_DB_connection()
    cursor = mydb.cursor()
    sql = "SELECT id FROM users WHERE email=%s"
    val = (email,)
    cursor.execute(sql, val)
    user_id = cursor.fetchone()
    cursor.close()
    mydb.close()
    if user_id == None:
        return None
    else:
        return user_id[0]


def get_subjects():
    mydb = get_DB_connection()
    cursor = mydb.cursor(buffered=True)
    query = "SELECT * FROM subjects"
    cursor.execute(query)
    result = cursor.fetchall()

    subjects = []
    for row in result:
        subject_dict = {
            'id': row[0],
            'kod': row[1],
            'ime': row[2],
            'bodovi': row[3],
            'godina': row[4]
        }
        subjects.append(subject_dict)

    cursor.close()
    mydb.close()
    return subjects