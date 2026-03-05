from flask import session, Flask, request, render_template, redirect, url_for, make_response
import subprocess
import urllib.parse
import sqlite3
import os

# Flask app config
app = Flask(__name__)
app.secret_key = 'not_easy'

DB_FILE = "users.db"

def init_db():
    if not os.path.exists(DB_FILE):
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute('''CREATE TABLE users (username TEXT PRIMARY KEY, password TEXT)''')
        c.execute("INSERT INTO users (username, password) VALUES ('admin@wctf.com', 'admin_super_secret_password_2026')")
        conn.commit()
        conn.close()

init_db()

@app.route("/")
def home():
	if 'user' in session:
		return redirect(url_for('sess'))
	return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
	if request.method == "POST":
		user = request.form['susername']
		pwd = request.form['spassword']
		confirm = request.form['spassword2']
		if pwd == confirm:
			if len(pwd) >= 6:
				try:
					conn = sqlite3.connect(DB_FILE)
					c = conn.cursor()
					c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (user, pwd))
					conn.commit()
					conn.close()
					return render_template("login.html", info="Registered successfully!")
				except sqlite3.IntegrityError:
					return render_template("login.html", info="Email already registered")
			else:
				return render_template("login.html", info="Password must be atleast 6 characters in Length")
		else:
			return render_template("login.html", info="The passwords you entered do not match!")


@app.route("/login", methods=["GET", "POST"])
def login():
	if request.method == "POST":
		user = request.form['username']
		pwd = request.form['password']
		conn = sqlite3.connect(DB_FILE)
		c = conn.cursor()
		c.execute("SELECT * FROM users WHERE username=? AND password=?", (user, pwd))
		account = c.fetchone()
		conn.close()
		if account:
			session["user"] = user
			session.permanent = True
			return redirect(url_for("sess"))
		else:
			return render_template("login.html", info="Invalid Email/password")

@app.route("/dashboard")
def sess():
	if 'user' not in session:
		return redirect(url_for('home'))
	mail = session['user']
	name = mail.split('@')[0].capitalize()
	cook = request.cookies.get('_ga')
	if cook == 'YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5':
		return render_template("dashboard.html", name=name ,flag='DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}')
	
	res = make_response(render_template('dashboard.html', name=name))
	if mail == "admin@wctf.com":
		res.set_cookie('_ga', 'YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5', max_age=60*60*24*365*2)		
	else:
		res.set_cookie('_ga', '25d55ad283aa400af464c76d713c07ad', max_age=60*60*24*365*2)
	return res

@app.route("/deshboard", methods=["GET", "POST"])
def fake_dashboard():
	if request.method == "GET":
		name = request.args.get('name')
		if name is None:
			return '''
			<pre>
@app.route("/deshboard", methods=["GET", "POST"])
def fake_dashboard():
        if request.method == "GET":
                name = request.args.get('name')
                if name is None:
                        return "" 
                        if request.method == "GET":
                                return redirect('dashboard')
                        if request.method == "POST":
                                name = request.args.get['name']
                        "" 
                else:   
                        return f"" Hello {name} ""
            </pre>
			'''
		else:	
			# Simple XSS Filter for Medium Difficulty
			blacklist = ['script', 'iframe', 'object', 'applet', 'embed', 'form']
			for tag in blacklist:
				if tag in name.lower():
					return '''
					<h1> WAF Blocked your payload: {} detected </h1>
					'''.format(tag)
			return '''
			<h1> Hello {} </h1>
			<!-- Nothing Here --> 
			'''.format(name)

@app.route("/report", methods=["GET", "POST"])
def report():
	if request.method == "GET":
		return render_template('report.html')
	
	if request.method == "POST":
		url = request.form.get('url')
		if not url:
			return render_template('report.html', info="Please provide a URL")
		
		# Basic check to avoid arbitrary navigation attacks
		# We expect the payload to be hosted on the same server, but we will allow it 
		# as long as it starts with http
		if not url.startswith('http'):
			return render_template('report.html', info="URL must start with http:// or https://")

		try:
			# Call the puppeteer bot in a subprocess
			# In a real CTF, this should be done via a task queue (e.g. Celery) to avoid blocking
			subprocess.Popen(['node', 'bot.js', url])
			return render_template('report.html', info="Admin is reviewing your link...")
		except Exception as e:
			print(e)
			return render_template('report.html', info="Error contacting Admin Bot")



@app.route("/test")
def tester():
  return render_template('dashboard.html')

@app.route("/logout")
def logout():
	session.pop("user", None)
	return redirect(url_for('home'))

if __name__ == "__main__":
  app.run(port=5007)

