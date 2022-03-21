#!C:\Users\Nikola\AppData\Local\Programs\Spyder\Python\python

import cgi
params = cgi.FieldStorage()
#first_name = params.getvalue("firstname")

lozinka = params.getvalue("password")
lozinka2 = params.getvalue("password2")

if(lozinka != lozinka2):
    print("Location: page1.py")

print ('''
<!DOCTYPE html>
<html>
<body>

<h2>Unesite podatke:</h2>

<form action="page3.py" method="post">
  Status: 
  <input type="radio" name="studij" value="izvanredni" checked> izvanredni studij
  <input type="radio" name="studij" value="redovni"> redovni studij<br>
  <br><br>
  E-mail:
  <input type="email" name="email" value=""> <br><br>
  Smjer:
  <select name="smjer_studija">
    <option value="programiranje">programiranje</option>
    <option value="baze_podataka">baze podataka</option>
    <option value="mreze">mreze</option>
    <option value="informacijski_sustavi">informacijski sustavi</option>
  </select><br>
  
  Zavrsni: <input type="checkbox" name="zavrsni" value="zavrsni">
<br><br>
  <br><br>''')
print ('<input type="hidden" name="firstname" value="' + params.getvalue("firstname") + '">')
print ('<input type="hidden" name="password" value="' + params.getvalue("password") + '">')
print ('''
<br>
<input type="submit" value="submit">
</form>

</body>
</html>''')
print("Ovako se zovu post parametri iz skripte koja se submit-ala na test3.py: ")
print (params.getvalue("firstname"))
print ('<br>')
print("Parametri pod ovim imenom ne postoje: ")
print (params.getvalue("ime"))
