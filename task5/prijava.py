#!python.exe
import base
import cgi
import session
import os
import db
import authentication
params = cgi.FieldStorage()

pass_error="Pogresna lozinka"
email_error="Korisnik nije pronaden"
pass_flag=False
email_flag=False
global_error=False

if (os.environ["REQUEST_METHOD"].upper() == "POST"):
    username = params.getvalue("username")
    password = params.getvalue("password")
    email = params.getvalue("email")
    uspilo=db.get_user(email, password)
    user_id=db.get_user_id(email)
    if user_id==None:
        email_flag=True
    if uspilo:
        user_id = db.get_user_id(email)
        db.get_or_create_session_id(str(user_id))
        print ('Location: index.py?email=" + email + "\r\n\r\n')


base.start_html()
print('''<form method="POST">''')
print('''<table>
    <tr><td>Email</td> <td><input type="text" name="email"><br></td></tr>
    <tr><td>Lozinka</td><td><input type="password" name="password"><br></td></tr>
    </table>
    <button type="submit" >Prijava</button>
    </form>
     ''')
print(user_id)
if os.environ["REQUEST_METHOD"].upper() == "POST" and not uspilo:
    if pass_flag:
        print(pass_error+"<br>")
    if email_flag:
        print(email_error+"<br>")

base.end_html()
