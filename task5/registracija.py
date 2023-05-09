#!python.exe

import base
import cgi, os
import authentication
import session

pass_error="Lozinke se ne podudaraju"
email_error="Email se vec koristi"
ime_error="Korisnicko ime se vec koristi"
pass_flag=False
email_flag=False
name_flag=False
global_error=False
params = cgi.FieldStorage()
if os.environ["REQUEST_METHOD"].upper() == "POST":
    #session.add_to_session(params)
    username = params.getvalue("username")
    password = params.getvalue("password")
    repeat = params.getvalue("repeat_password")
    email = params.getvalue("email")
    email_flag=authentication.check_email(email)
    name_flag=authentication.check_username(username)
    if password == repeat and email_flag==False and name_flag==False:
        pass_flag=False
        success = authentication.register(username, email, password)
        if success:
            print('Location: prijava.py')
    else:
        global_error=True
print()
base.start_html()
print ('''<form class="register-form" method="POST">
<h2>REGISTER</h2>
username <input type="text" name="username" /><br>
email <input type="text" name="email" /><br>
password <input type="password" name="password"/><br>
Repeat password <input type="password" name="repeat_password"/><br>
<input type="submit" value="Register"/>
</form>''')
print('<a class="btn" href="prijava.py">Login</a><br>')
if os.environ["REQUEST_METHOD"].upper() == "POST" and global_error:
    if pass_flag:
        print(pass_error+"<br>")
    if email_flag:
        print(email_error+"<br>")
    if name_flag:
        print(ime_error+"<br>")
        
base.end_html()