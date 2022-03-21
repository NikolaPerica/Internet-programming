#!C:\Users\Nikola\AppData\Local\Programs\Spyder\Python\python

import cgi
#form_data = cgi.FieldStorage()
params = cgi.FieldStorage()

print ('''
<!DOCTYPE html>
<html>
<body>

<h2>Uneseni podatci:</h2>

''')

print ('Ime: '+ params.getvalue("firstname"))
print ('<br>Email: ' + params.getvalue("email"))
print ('<br>Studij: ' + params.getvalue("studij"))
print ('<br> Smjer: ' + params.getvalue("smjer_studija"))
print ('<br>Zavrsni rad: ' + params.getvalue("zavrsni"))
print ('<br>Napomene: ' + params.getvalue("napomene"))

print ('''
<br><br><br>
<a href='page1.py'>Na pocetak</a>

</body>
</html>''')
