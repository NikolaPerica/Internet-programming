#!python.exe
import base
import cgi
import db

def student_list():
    print("""
            <form action="" method="post">
                <table>
    """)
    for key, value in lista_studenata.items():
        print(f"""
                    <tr>
                        <td><a href='/cgi-bin/vj6/upisni_list.py?student_id={key}'>{value}</a></td>
                    </tr>
        """)
    print("""
                </table>
            </form>

    """)
        
params = cgi.FieldStorage()
email = params.getvalue("email")

user_id = db.get_user_id(email)
lista_studenata = db.get_all_students()
subjects_list = db.get_subjects()

base.start_html()
student_list()
print('&nbsp&nbsp<a class="btn" href="index.py">Back</a><br>')
base.end_html()