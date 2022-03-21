#!C:\Users\Nikola\AppData\Local\Programs\Spyder\Python\python

import cgi
import os
import cgitb
cgitb.enable(display=0, logdir="")

print  ("""
<!DOCTYPE html>
<html>
<body>
<h2>Unesite podatke:</h2>
<form action="page2.py" method="post">
  Ime: 
  <input type="text" name="firstname" value="">
  <br>
  Lozinka: 
  <input type="password" name="password" value=""><br>
  Ponoviti lozinku: 
  <input type="password" name="password2" value="">
  <br><br>
  <input type="submit" value="Submit">
</form> 


</body>
</html>
""")

params = cgi.FieldStorage() 
#print (params)
print (os.environ['REQUEST_METHOD'])
print ("<br>")
if os.environ['REQUEST_METHOD'].upper() == 'POST':
    print (params.getvalue("firstname"))
else:
    print(params.getvalue("lastname"))
