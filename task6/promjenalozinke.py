#!python.exe
import cgi
import os
import db
import base

def register():
    print("""

            <form action="" method="post">
                <table>
                    <tr>
                        <td><label for="current">Current Password: </label></td>
                        <td><input type="text" id="current" name="current"></td>
                    </tr>
                    <tr>
                        <td><label for="new_password">New Password: </label></td>
                        <td><input type="text" id="new_password" name="new_password"></td>
                    </tr>
                    <tr>
                        <td><label for="repassword">Retype new Password: </label></td>
                        <td><input type="password" id="repassword" name="repassword"></td>
                    </tr>

                </table>
                <input type="submit" name="mainPage" value="Back">
                <input type="submit" name="change" value="Change password">
            </form>
           
        
        """)

params = cgi.FieldStorage()
email = params.getvalue("email")

user_id = db.get_user_id(email)
mydb = db.get_DB_connection()
session_id = db.get_or_create_session_id(user_id)

base.start_html()    
if os.environ['REQUEST_METHOD'] == 'POST':
        if params.getvalue("change") == "Change password":
            current = params.getvalue("current")
            new_password = params.getvalue("new_password")
            repassword = params.getvalue("repassword")
            if not (current and new_password and repassword):
                print("<p>Prazan unos</p>")
            if new_password != repassword:
                print("<p>Nove sifre se ne podudaraju</p>")
            else:
                if(db.check_password(session_id, current)):
                    db.change_password(session_id, new_password)
                    print("<p>Sifra promijenjena</p>")
                else:
                   print("<p>Krivi unos glavne sifre</p>")
            

        elif params.getvalue("mainPage") == "Back":
            print("Location: index.py?email=" + email + "\r\n\r\n")

   
register()
base.end_html()