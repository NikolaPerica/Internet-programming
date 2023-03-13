#!C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python37_64\python.exe
#!python.exe
import subjects
import os
import cgi
import base
from http import cookies
values=cgi.FieldStorage()

def decide_subject_status(subject_key,values):
    cookies_string=os.environ.get('HTTP_COOKIE','')
    all_cookies_object=cookies.SimpleCookie(cookies_string)
    if(values.getvalue(subject_key)):
        return values.getvalue(subject_key)
    status=""
    if (all_cookies_object.get(str(subject_key))):
        status=all_cookies_object.get(str(subject_key)).value
    return status

def set_cookie_state(values):
    for key in values:
        cookie=cookies.SimpleCookie()
        cookie[str(key)]=values.getvalue(str(key))
        print(cookie.output())
        
def display_subjects_and_choices(year,values):
    print("<table style=""border: 1px solid"">")
    
    if (year=="list"):
        print("<tr>")
        print("<td >")
        print('''Svi predmeti''')
        print("</td>")
        print("<td colspan=""3"">")
        print("Status")
        print("</td>")
        print("</tr>")
        for key in subjects.subjects:
            print("<tr>")
            print("<td>")
            print(subjects.subjects[key]['name'])
            print("</td>")
            status=decide_subject_status(key,values)
            for status_key in subjects.status_names:
                if(status==status_key):
                    print("<td>")
                    print('''<input type="radio" name="'''+key+'''" value="'''+status_key+'''" checked="checked">'''+subjects.status_names[status_key])
                    print("</td>")
                else:
                    print("<td>")
                    print('''<input type="radio" name="'''+key+'''" value="'''+status_key+'''">'''+subjects.status_names[status_key])
                    print("</td>")
            print("</tr>")
    else:
        print("<tr>")
        print("<td>")
        print(year+'''. Godina''')
        print("</td>")
        print("<td colspan=""3"">")
        print("Status")
        print("</td>")
        print("</tr>")
        for key in subjects.subjects:
            if(str(subjects.subjects[key]['year'])==year):
                print("<tr>")
                print("<td>")
                print(subjects.subjects[key]['name'])
                print("</td>")
                status=decide_subject_status(key,values)
                for status_key in subjects.status_names:
                    if(status==status_key):
                        print("<td>")
                        print('''<input type="radio" name="'''+key+'''" value="'''+status_key+'''" checked="checked">'''+subjects.status_names[status_key])
                        print("</td>")
                    else:
                        print("<td>")
                        print('''<input type="radio" name="'''+key+'''" value="'''+status_key+'''">'''+subjects.status_names[status_key])
                        print("</td>")

                print("</tr>")
    print("</table>")


def display_form(values,year="1"):
    print('''<form method="POST">''')
    display_subjects_and_choices(year,values)
    print('''
    <!---<button type="submit" name="submit">Submit</button>--->
    <button type="submit" name="year" value="1">Prva godina</button>
    <button type="submit" name="year" value="2">Druga godina</button>
    <button type="submit" name="year" value="3">Treca godina</button>
    <button type="submit" name="year" value="list">Upisni list</button>
    </form>
     ''')

set_cookie_state(values)
base.start_html()
#print(values)
if(values.getvalue("year")):
    display_form(values,values.getvalue("year"))
else:
    display_form(values)
base.stop_html()