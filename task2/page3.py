#!C:\Users\Nikola\AppData\Local\Programs\Spyder\Python\python

import cgi
params = cgi.FieldStorage()

if(params.getvalue("zavrsni") == "zavrsni"):
  test = "Da"
else:
  test = "Ne"  


print ('''
<!DOCTYPE html>
<html>
<body>

<h2>Unesite podatke:</h2>
<form action="print.py" method="post">
  Napomene: <input type="text" name="napomene" value=" ">
  <br><br>''')
print ('<input type="hidden" name="firstname" value="' + params.getvalue("firstname") + '">')
print ('<input type="hidden" name="studij" value="' + params.getvalue("studij") + '">')
print ('<input type="hidden" name="email" value="' + params.getvalue("email") + '">')
print ('<input type="hidden" name="smjer_studija" value="' + params.getvalue("smjer_studija") + '">')
print ('<input type="hidden" name="zavrsni" value="' + test + '">')
#print(test)
print ('''
<br>
<input type="submit" value="submit">
</form>

</body>
</html>''')
print (params.getvalue("smjer_studija"))
print ('<br>')
print (params.getvalue("firstname")) 
