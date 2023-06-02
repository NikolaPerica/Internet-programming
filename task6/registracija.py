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
    role = params.getvalue("role")
    email_flag=authentication.check_email(email)
    name_flag=authentication.check_username(username)
    if password == repeat and email_flag==False and name_flag==False:
        pass_flag=False
        success = authentication.register(username, email, password, role)
        if success:
            print('Location: prijava.py')
    else:
        global_error=True
print()
base.start_html()
print ('''<form class="register-form" method="POST">
<table>
<h2>REGISTER</h2>
<tr>
    <td>username</td> <td><input type="text" name="username" /></td>
</tr>
<tr>
    <td>email</td> <td><input type="text" name="email" /></td>
</tr>
<tr>
<td>password</td><td> <input type="password" name="password"/></td>
</tr>
<tr>
<td>Repeat password</td><td> <input type="password" name="repeat_password"/></td>
</tr>
<tr>
<td><label>Uloga: </label> </td>
<td><input type="radio" id="admin" name="role" value="admin">
<label for="admin">Admin
<input type="radio" id="student" name="role" value="student" checked>
<label for="student">Student</label>
</td>
</tr>
</table>
<br>
<input type="submit" value="Register"/>
&nbsp&nbsp<a class="btn" href="prijava.py">Login</a><br>
</form>''')

if os.environ["REQUEST_METHOD"].upper() == "POST" and global_error:
    if pass_flag:
        print(pass_error+"<br>")
    if email_flag:
        print(email_error+"<br>")
    if name_flag:
        print(ime_error+"<br>")
        
base.end_html()