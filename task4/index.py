#!python.exe
import subjects
import os
import cgi
import base
import session
from http import cookies
values=cgi.FieldStorage()
session_data = session.get_session_data()

if (os.environ["REQUEST_METHOD"].upper() == "POST"):
    session.add_to_session(values)

#def subject_status(subject_key,values):
 #   cookies_string=os.environ.get('HTTP_COOKIE','')
  #  all_cookies_object=cookies.SimpleCookie(cookies_string)
   # if(values.getvalue(subject_key)):
    #    return values.getvalue(subject_key)
   # status=""
   # if (all_cookies_object.get(str(subject_key))):
    #    status=all_cookies_object.get(str(subject_key)).value
    #return status

def get_year(values):
    if(values.getvalue("year")):
        return values.getvalue("year")
    year=""
    if (session_data.get(str("year"))):
        year=session_data.get(str("year")).value
    return year

def set_cookie_state(values):
    for key in values:
        cookie=cookies.SimpleCookie()
        cookie[str(key)]=values.getvalue(str(key))
        print(cookie.output())

def printAll(values):
    total_ects=0
    print("<tr>")
    print("<td >")
    print('''Svi predmeti''')
    print("</td>")
    print("<td>")
    print("Status")
    print("</td>")
    print("<td>")
    print("ECTS")
    print("</td>")
    print("</tr>")
    for sub, stat_name in session_data.items():
        if(subjects.subjects.get(sub)!=None):
            print('<tr>')
            print('<td>'+subjects.subjects.get(sub)['name']+'</td>')
            print('<td>'+subjects.status_names[stat_name]+'</td>')
            print('<td>'+str(subjects.subjects.get(sub)['ects'])+'</td>')
            print('</tr>')
            if(stat_name=="pass"):
                total_ects+=subjects.subjects.get(sub)['ects']
    print('''<tr><td></td><td>Ukupno:</td><td>'''+str(total_ects)+'''</td></tr>''')


def printYear(year, values):
    print("<tr>")
    print("<td>")
    print(year+'''. Godina''')
    print("</td>")
    print("<td colspan=""3"">")
    print("Status")
    print("</td>")


    for key, value in subjects.subjects.items():
        if(str(subjects.subjects[key]['year'])==year):
            print('<tr>')
            print('<td>'+value['name']+'</td>')
            current_stat = session_data.get(key, 'not') # spremi u current stat trenutni status, a ako ga nema onda not
            for stat, stat_name in subjects.status_names.items():
                if current_stat == stat:
                    print("<td>")
                    print('<input type="radio" name="' + key + '" value="' + stat + '" checked > ' + stat_name)
                    print("</td>")
                else:
                    print("<td>")
                    print('<input type="radio" name="' + key + '" value="' + stat + '" > ' + stat_name)
                    print("</td>")
            print('</tr>')

def display_subjects_and_choices(year, values):
    print("<table>")
    if (year=="list"):
        printAll(values)
    else:
        printYear(year, values)
    print("</table>")
    

def display_form(values):
    year = get_year(values)
    
    if(year==""):
        year="1"
    print('''<form method="POST">''')
    display_subjects_and_choices(year,values)
    print('''
    <button type="submit" name="year" value="1">Prva godina</button>
    <button type="submit" name="year" value="2">Druga godina</button>
    <button type="submit" name="year" value="3">Treca godina</button>
    <button type="submit" name="year" value="list">Upisni list</button>
    </form>
     ''')

set_cookie_state(values)
base.start_html()
display_form(values)
base.end_html()