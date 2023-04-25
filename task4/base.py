#!python.exe
def start_html():
    print("""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        table, th, td {
            border: 1px solid;
           <!---border-collapse: collapse;--->
        }
        </style>
    </head>
    <body>
     """)

def end_html():
    print("""</body>
    </html>
    """)