#!python.exe
import cgi
import os
import db

def register():
    print("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <style>
        table, th, td {
            border:1px solid black;
            }
        </style>
        </head>
        <body>
            <form action="" method="post">
                <table>
                    <tr>
                        <th><label for="current">Current Password: </label></th>
                        <th><input type="text" id="current" name="current"></th>
                    </tr>
                    <tr>
                        <th><label for="new_password">New Password: </label></th>
                        <th><input type="text" id="new_password" name="new_password"></th>
                    </tr>
                    <tr>
                        <th><label for="repassword">Retype new Password: </label></th>
                        <th><input type="password" id="repassword" name="repassword"></th>
                    </tr>
                    <tr>
                        <th><input type="submit" name="mainPage" value="Back"></th>
                        <th><input type="submit" name="change" value="Change password"></th>
                    </tr>
                </table>
            </form>
            """ + message + """
        </body>
        </html>
        """)

params = cgi.FieldStorage()
email = params.getvalue("email")

user_id = db.get_user_id(email)
mydb = db.get_DB_connection()
session_id = db.get_or_create_session_id(user_id)

message = ""
if os.environ['REQUEST_METHOD'] == 'POST':
        if params.getvalue("change") == "Change password":
            current = params.getvalue("current")
            new_password = params.getvalue("new_password")
            repassword = params.getvalue("repassword")
            if not (current and new_password and repassword):
                message = "<p>Prazan unos</p>"
            if new_password != repassword:
                message = "<p>Nove sifre se ne podudaraju</p>"
            

        elif params.getvalue("mainPage") == "Back":
            print("Location: index.py?email=" + email + "\r\n\r\n")

              
register()