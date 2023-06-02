#!python.exe
import cgi
import base
import db

def print_upisni_list():
    total_ects = 0
    print("""
            <table>
                <tr>
                    <th><label for="fname">Predmet</label></th>
                    <th><label for="password">Status</label></th>
                    <th><label for="password">Bodovi</label></th>
                </tr>""")
    for subject in subjects:
        status = upisni_list_dict.get(subject['kod'])
        if status == 'enr':
            status = 'Enrolled'
            total_ects += subject['bodovi']
        elif status == 'pass':
            status = 'Passed'
        else:
            status = 'Not selected'
        print("""
            <tr>
                <td><label for="fname">""" + subject['ime'] + """</label></td>
                <td>""" + status + """</td>
                <td><label for="fname">""" + str(subject['bodovi']) + """</label></td>
            </tr>""")
    print("""
            <tr>
                <td></td>
                <td>Ukupno: </td>
                <td><label for="fname">""" + str(total_ects) + """</label></td>
            </tr>
    """)
    print("</table>")

params = cgi.FieldStorage()
email = params.getvalue("email")
student_id = params.getvalue("student_id")

upisni_list_dict = db.get_data(student_id)
subjects = db.get_subjects()


base.start_html()
print_upisni_list()
print('&nbsp&nbsp<a class="btn" href="popis_studenata.py">Back</a><br>')
base.end_html()
