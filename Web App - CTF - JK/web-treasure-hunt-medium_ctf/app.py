from flask import Flask, request, redirect, render_template, session

app = Flask(__name__)
app.secret_key = 'super_secret_medium_treasure_hunt_2026'

EASY_FLAG = "DAKSHH{h1nglish_hunt_3asy}"
MEDIUM_FLAG = "DAKSHH{css_gh0st_m3d1um}"

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("password") == EASY_FLAG:
        session['authenticated'] = True
        return redirect("/stage1")
    return render_template('error.html', error_title="ACCESS DENIED", error_msg="Incorrect Key. You must clear the Easy Hunt first.", back_url="/")

@app.route("/stage1")
def stage1():
    if not session.get('authenticated'):
        return redirect("/")
    return render_template('stage1.html')

@app.route("/hidden_shadow")
def shadow():
    if not session.get('authenticated'):
        return redirect("/")
    return render_template('shadow.html')

@app.route("/vault", methods=["POST", "GET"])
def vault():
    if not session.get('authenticated'):
        return redirect("/")
        
    if request.method == "POST":
        if request.form.get("passkey") == "k3y_m4st3r_2026":
            session['vault_unlocked'] = True
            return redirect("/vault")
        return render_template('error.html', error_title="DECRYPTION FAILED", error_msg="Incorrect Vault Password.", back_url="/hidden_shadow")
        
    if session.get('vault_unlocked'):
        return render_template('vault.html', flag=MEDIUM_FLAG)
    
    return redirect("/hidden_shadow")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
