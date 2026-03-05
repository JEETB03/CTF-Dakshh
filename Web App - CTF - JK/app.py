from flask import Flask, render_template, request
import os
import sqlite3
import base64

app = Flask(__name__)
DB_FILE = "challenge.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
  return render_template("index.html")

#random hidden path to create db table
@app.route("/iusdyfuhu")
def initial():
  conn = get_db_connection()
  cur = conn.cursor()

  cur.execute('''
  create table if not exists users (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username varchar(100),
  password varchar(100)
  );
  ''')
  cur.execute("insert into users (username, password) select 'admin', 'secret_password_do_not_guess' where not exists (select 1 from users where username='admin')")

  conn.commit()
  cur.close()
  conn.close()
  return "Table created successfully!!"

@app.route("/register", methods=["POST"])
def register():
  user = request.form.get('user', '')
  pwd = request.form.get('pass', '')

  if user == 'admin':
    return render_template("index.html", data="You can't register with admin username")

  if '/static/flag.png' in user:
    user = user.replace("flag.png", "flag2.png")

  user = user.replace("=", "").replace("/", "").replace(";", "")

  conn = get_db_connection()
  cur = conn.cursor()

  try:
      cur.execute(f"insert into users (username, password) values ('{user}', '{pwd}'); ")
      conn.commit()
      msg = "Registered successfully !"
  except Exception as e:
      msg = "Registration Error: " + str(e)
  finally:
      cur.close()
      conn.close()
  return render_template("index.html", data=msg)

@app.route("/login", methods=["POST"])
def login():
  conn = get_db_connection()
  cur = conn.cursor()

  user = request.form.get("user", "")
  pwd = request.form.get("pass", "")

  if '/static/flag.png' in user:
    user = user.replace("flag.png", "flag2.png")

  try:
    cur.execute(f"select * from users where username='{user}' and password='{pwd}';")
    t = cur.fetchall()

    conn.commit()
    cur.close()
    conn.close()

    if t:
      if str(t[0]['username']) == 'admin':
        return '''
<center>
<h1> WELCOME ADMIN </h1>
<br><br>
<h3>
You bypassed the authentication successfully!
</h3>
<br><br>
<h2>Flag: DAKSHH{sqli_3asy_byP4ss_2026}</h2>
</center>
'''
      else:
        return "Hello " + str(t[0]['username'])
    else:
        return render_template("index.html", data="Invalid Login/Password !!")

  except Exception as e:
    print(str(e))
    return render_template("index.html", data="Invalid Login/Password !!")

@app.route("/static/flag.png")
def forbide():
    return '''
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
<title>404 Not Found</title>
<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
'''

@app.route("/sqleditor")
def editor():
  return '''
<center>
<h1>SQL Editor</h1>
<br><br>
<form action="output" method="post">
<textarea name="sql" rows="15" cols="60">
Enter query here
</textarea>
<br><br><br>
<input type=submit value="Execute">
</form>
</center>
'''

@app.route("/output", methods=["POST"])
def creator():
  code = request.form.get('sql', '')
  conn = get_db_connection()
  cur = conn.cursor()
  res = ''

  if 'insert' in code.lower() or 'delete' in code.lower() or 'update' in code.lower():
    try:
      cur.execute(code)
      conn.commit()
      cur.close()
      conn.close()
      return "Insertion/Deletion/updation of data sucessful !!"
    except Exception as e:
      return "Some Error occured in your SQL code : " + str(e)

  try:
    cur.execute(code)
    t = cur.fetchall()
  except Exception as e:
    return "Some Error occured in your SQL code : " + str(e)

  for i in t:
    res = res + str(dict(i)) + "<br>"

  conn.commit()
  cur.close()
  conn.close()
  return res

if __name__ == "__main__":
  app.run(debug=True, port=5001)
