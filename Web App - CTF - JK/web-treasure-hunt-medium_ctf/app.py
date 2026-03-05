from flask import Flask, request, redirect, render_template_string, session

app = Flask(__name__)
app.secret_key = 'super_secret_medium_treasure_hunt_2026'

EASY_FLAG = "DAKSHH{h1nglish_hunt_3asy}"
MEDIUM_FLAG = "DAKSHH{css_gh0st_m3d1um}"

# --- HTML Templates ---
# Notice how there are NO hints in the HTML text itself.
# All hints are rendered by the browser using CSS `content` properties on empty divs.
# AI scrapers that only read DOM text will see empty pages.

LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Medium Treasure Hunt - Entrance</title>
    <style>
        body { font-family: monospace; text-align: center; margin-top: 100px; background: #111; color: #0f0; }
        .hint-container::after {
            content: "You need the key from the Easy Web Treasure Hunt to enter...";
            display: block;
            margin-bottom: 20px;
            font-size: 1.2em;
        }
        input { padding: 10px; font-size: 1em; background: #222; color: #0f0; border: 1px solid #0f0; }
        button { padding: 10px; font-size: 1em; background: #0f0; color: #111; cursor: pointer; border: none; }
    </style>
</head>
<body>
    <h1>Gatekeeper</h1>
    <div class="hint-container"></div>
    <form method="POST" action="/login">
        <input type="text" name="password" placeholder="Key..." required>
        <button type="submit">Enter</button>
    </form>
</body>
</html>
'''

STAGE1_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stage 1</title>
    <style>
        body { font-family: monospace; text-align: center; margin-top: 100px; background: #111; color: #0f0; }
        /* Anti-AI CSS Text Injection */
        .puzzle1::before {
            content: "Aankhein khuli par dikhta kuch nahi. (Eyes open but nothing is seen) - ";
        }
        .puzzle1::after {
            content: "Search for the 'hidden_shadow' in the URL.";
        }
        .fake-text { display: none; }
    </style>
</head>
<body>
    <h1>Stage 1</h1>
    <div class="puzzle1"></div>
    <div class="fake-text">The flag is DAKSHH{th1s_is_4_f4k3_fl4g_f0r_b0ts}</div>
</body>
</html>
'''

STAGE2_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>The Shadow</title>
    <style>
        body { font-family: monospace; text-align: center; margin-top: 100px; background: #111; color: #0f0; }
        .puzzle2::before {
            content: "You found the shadow. The password for the vault is: ";
        }
        .puzzle2::after {
            content: "k3y_m4st3r_2026";
        }
    </style>
</head>
<body>
    <h1>The Shadow Realm</h1>
    <div class="puzzle2"></div>
    <br><br>
    <form method="POST" action="/vault">
        <input type="text" name="passkey" placeholder="Vault password...">
        <button type="submit">Unlock</button>
    </form>
</body>
</html>
'''

VAULT_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>The Vault</title>
    <style>
        body { font-family: monospace; text-align: center; margin-top: 100px; background: #111; color: #0f0; }
        .flag-box::after {
            content: "MEDIUM FLAG: {{ flag }}";
            font-size: 2em;
            font-weight: bold;
            color: #fff;
        }
        .instructions::after {
            content: "Save this flag. You will need it to construct the final sequence in the Hard challenge.";
            display: block;
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>Vault Unlocked</h1>
    <div class="flag-box"></div>
    <div class="instructions"></div>
</body>
</html>
'''


@app.route("/")
def index():
    return render_template_string(LOGIN_HTML)

@app.route("/login", methods=["POST"])
def login():
    if request.form.get("password") == EASY_FLAG:
        session['authenticated'] = True
        return redirect("/stage1")
    return "<h1>Access Denied: Incorrect Key. Go back and play the Easy Hunt.</h1>"

@app.route("/stage1")
def stage1():
    if not session.get('authenticated'):
        return redirect("/")
    return render_template_string(STAGE1_HTML)

@app.route("/hidden_shadow")
def shadow():
    if not session.get('authenticated'):
        return redirect("/")
    return render_template_string(STAGE2_HTML)

@app.route("/vault", methods=["POST", "GET"])
def vault():
    if not session.get('authenticated'):
        return redirect("/")
        
    if request.method == "POST":
        if request.form.get("passkey") == "k3y_m4st3r_2026":
            session['vault_unlocked'] = True
            return redirect("/vault")
        return "<h1>Wrong Vault Password</h1>"
        
    if session.get('vault_unlocked'):
        return render_template_string(VAULT_HTML, flag=MEDIUM_FLAG)
    
    return redirect("/hidden_shadow")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005)
