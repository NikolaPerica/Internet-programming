#!python.exe
import cgi
import os
import base
import subjects
import db
import session

accessFlag=False

def main_page():
    print("""
    <p>Hej """+db.get_name(session_id)+"""!</p>
        <form action="" method="post">
            <table>
                  <tr>
                    <th><input type="submit" name="odjava" value="Odjava" /></th>
                    <th><input type="submit" name="promjeni_lozinku" value="Promjeni lozinku" /></th>
                    <th><input type="submit" name="popis_studenata" value="Popis studenata" /></th>
                </tr>
              
            </table>
        </form>
    """)

def print_navigation():
    print("""
        <form action="" method="post">
            <div class="tab">
                <input type="submit" name="year" value="1st Year">
                <input type="submit" name="year" value="2nd Year">
                <input type="submit" name="year" value="3rd Year">
                <input type="submit" name="year" value="Upisni List">
                <br>
            </div>
    """)

def print_table(year):
        year_name = ""
        if year == None or year == "1st Year":
            year = 1
            year_name = "1st Year"
        elif year == "2nd Year":
            year = 2
            year_name = "2nd Year"
        elif year == "3rd Year":
            year = 3
            year_name = "3rd Year"
        else:
            print_upisni_list()
            return
        print("""
            <table>
                <tr>
                    <th><label for="fname">""" + year_name + """</label></th>
                    <th><label for="password">Ects</label></th>
                    <th><label for="password">Status</label></th>
                </tr>""")
        for subject in subjects_list:
            if subject['godina'] == year:
                print("""
                    <tr>
                        <td><label for="fname">""" + subject['ime'] + """</label></td>
                        <td><label for="fname">""" + str(subject['bodovi']) + """</label></td>
                        <td>""")
                default_value = 'not'
                for key, value in subjects.status_names.items():
                    checked = ''
                    if subject['kod'] in upisni_list_dict and upisni_list_dict[subject['kod']] == key:
                        checked = 'checked'
                    else:
                        checked = 'checked' if key == default_value else ''
                    print(f"""
                            <input type="radio" id="{key}" name="{subject['kod']}" value="{key}" {checked}>
                            <label for="{key}">{value}</label>""")
                print("""
                        </td>
                    </tr>""") 
        print("""</table>
        </form>""")
        print("""</table>
        </form>""")

def print_upisni_list():
    total_ects = 0
    print("""
            <table>
                <tr>
                    <th><label for="fname">Predmet</label></th>
                    <th><label for="password">Status</label></th>
                    <th><label for="password">Bodovi</label></th>
                </tr>""")
    for subject in subjects_list:
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
year = params.getvalue("year")

user_id = db.get_user_id(email)
session_id = db.get_or_create_session_id(user_id)
data_dict= db.get_data(session_id)


for p in params.keys():
    if p not in ['email', 'year']:
        status = params[p].value
        db.add_to_upisni_list(p, session_id, status)
upisni_list_dict = db.get_data(session_id)
subjects_list = db.get_subjects()


if os.environ['REQUEST_METHOD'] == 'POST':
    if params.getvalue("odjava") == "Odjava":
        session.logout()
        print("Location: prijava.py\r\n\r\n")
    
    elif params.getvalue("promjeni_lozinku") == "Promjeni lozinku":
        print("Location: promjenalozinke.py?email=" + email + "\r\n\r\n")
    elif params.getvalue("popis_studenata") == "Popis studenata":
        if(db.check_role(session_id)):
            print("Location: popis_studenata.py?email=" + email + "\r\n\r\n")
        else:
            accessFlag=True

base.start_html()

main_page()
print("<br>")
if os.environ['REQUEST_METHOD'] == 'POST':
    if(accessFlag==True):
        print("Nemate pravo pristupa")
print_navigation()
print("<br>")
print_table(year)
base.end_html()
#print(session_dict)
