from flask import Flask,request,redirect,render_template
from os import system
import os

app = Flask(__name__)

@app.route("/")
def wel():
  return render_template('index.html')

#111
@app.route("/gmdost")
def sss():
  return render_template('gmdost.html')

#222
@app.route("/429")
def bomb():
  return render_template('429.html'), 404

#333
@app.route("/yagf")
def login():
  return render_template('yagf.html')

#444
@app.route("/validate", methods=["GET","POST"])
def check():
  if request.method == "GET":
   return render_template('error.html', error_title="403 FORBIDDEN", error_msg="You are not authorized to view this page directly.")
  if request.method == "POST":
   form_data = request.form
   usr = form_data.get('usr', '')
   pwd = form_data.get('pwd', '')

   if usr == 'ami_hacker_bolchi' and pwd == 'hitk_system_h4cked':
    return redirect("/finalpath", code=302)
   else:
    return render_template('error.html', error_title="AUTH FAILED", error_msg="Invalid Login Credentials.", back_url="/yagf")

#555
@app.route("/finalpath")
def last():
  return render_template('final.html')

@app.route("/redirect", methods=["GET", "POST"])
def cmcheck():
  if request.method == 'GET':
    return render_template('error.html', error_title="403 FORBIDDEN", error_msg="Direct access restricted. Submit commands via the terminal.")
  if request.method == 'POST':
    form_data = request.form
    if form_data['cmd'] == 'ls' or form_data['cmd'] == 'cat flagpath' or form_data['cmd'] == 'cat flag' or form_data['cmd'] == 'cat flag.txt':
      cmd = form_data['cmd']
      import platform
      if platform.system() == "Windows":
          if cmd.startswith("cat "):
              cmd = "type " + cmd[4:]
          elif cmd == "ls":
              cmd = "dir"
      try:
          import os
          a = os.popen(cmd).read()
      except Exception as e:
          a = "Error reading response: " + str(e)
      return render_template('final.html', output=str(a))
    else:
      return redirect("/finalpath", code=302)

@app.route("/dshgfayiurhaejkhbdsajvn")
def winner():
  return render_template('error.html', error_title="MISSING PARAMETER", error_msg="Go to /dshgfayiurhaejkhbdsajvn/{YOUR_NAME}")

@app.route("/dshgfayiurhaejkhbdsajvn/<name>")
def winnerfirst(name):
  return render_template('winner.html', name=name.upper())

@app.route("/hall-of-fame")
def hall():
  return '''
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
* {
  box-sizing: border-box;
}

body {
  margin: 0;
  font-family: Arial;
}

/* The grid: Four equal columns that floats next to each other */
.column {
  float: left;
  width: 25%;
  padding: 10px;
}

/* Style the images inside the grid */
.column img {
  opacity: 0.8; 
  cursor: pointer; 
}

.column img:hover {
  opacity: 1;
}

/* Clear floats after the columns */
.row:after {
  content: "";
  display: table;
  clear: both;
}

/* The expanding image container */
.container {
  position: relative;
  display: none;
}

/* Expanding image text */
#imgtext {
  position: absolute;
  bottom: 15px;
  left: 15px;
  color: white;
  font-size: 20px;
}

/* Closable button inside the expanded image */
.closebtn {
  position: absolute;
  top: 10px;
  right: 15px;
  color: white;
  font-size: 35px;
  cursor: pointer;
}
</style>
</head>
<body>

<div style="text-align:center">
  <h1>🥳 CTF WINNERS 🥳</h1>
  <p>Click on the images below</p>
</div>

<!-- The four columns -->
<div class="row">
  <div class="column">
    <img src="http://transfer.sh/1iAWBUS/jopraveen.jpeg" alt="Jopraveen" style="width:100%" onclick="myFunction(this);">
  </div>
  <div class="column">
    <img src="http://transfer.sh/1LUaRAd/paul.jpeg" alt="Paul" style="width:100%" onclick="myFunction(this);">
  </div>
  <div class="column">
    <img src="http://transfer.sh/DR52/sakthi.jpeg" alt="sakthi" style="width:100%" onclick="myFunction(this);">
  </div>
</div>

<div class="container">
  <span onclick="this.parentElement.style.display='none'" class="closebtn">&times;</span>
  <img id="expandedImg" style="width:100%">
  <div id="imgtext"></div>
</div>

<script>
function myFunction(imgs) {
  var expandImg = document.getElementById("expandedImg");
  var imgText = document.getElementById("imgtext");
  expandImg.src = imgs.src;
  imgText.innerHTML = imgs.alt;
  expandImg.parentElement.style.display = "block";
}
</script>

</body>
</html>

'''

if __name__ == "__main__":
   port = int(os.environ.get("PORT", 5004))
   app.run(host="0.0.0.0", port=port)
