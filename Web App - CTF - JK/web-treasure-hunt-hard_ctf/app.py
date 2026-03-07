import json
from flask import Flask, request, jsonify, render_template, make_response, redirect, session

app = Flask(__name__)
app.secret_key = 'hard_treasure_hunt_2026'

MEDIUM_FLAG_CONTENT = "css_gh0st_m3d1um"
HARD_FRAGMENT = "h4rd_fr4gm3nt_b0ss"
FINAL_FLAG = f"DAKSHH{{{MEDIUM_FLAG_CONTENT}_{HARD_FRAGMENT}}}"

@app.route("/", methods=["GET"])
def index():
    return render_template('index.html')

# The Core API Sequence
@app.route("/api/core", methods=["GET", "OPTIONS", "PATCH"])
def api_core():
    if request.method == "OPTIONS":
        # Step 1: OPTIONS request reveals what to PATCH
        resp = make_response(jsonify({"message": "Core API ready for configuration."}))
        resp.headers['X-Configuration-Required'] = 'Send PATCH request with JSON: {"status":"ready"}'
        return resp
        
    elif request.method == "PATCH":
        # Step 2: PATCH configures the core
        if request.is_json:
            data = request.get_json()
            if data.get("status") == "ready":
                resp = make_response(jsonify({"message": "Core synchronized. Proceed to GET."}))
                resp.set_cookie('core_session', 'synchronized')
                return resp
        return jsonify({"error": "Invalid configuration data."}), 400
        
    elif request.method == "GET":
        # Step 3: GET retrieves the hard fragment (only if session is synchronized)
        if request.cookies.get('core_session') == 'synchronized':
            return jsonify({
                "success": True, 
                "fragment_name": "Hard Fragment",
                "fragment_value": HARD_FRAGMENT,
                "instruction": "Combine this with the content inside the Medium Flag to craft the final flag."
            })
        else:
             return jsonify({"error": "Core not synchronized. Complete the required API sequence."}), 403

@app.route("/submit", methods=["POST", "GET"])
def submit():
    if request.method == "GET":
        # Check if they are trying to direct-route to success page
        if not session.get('authorized_win'):
            return render_template('error.html', error_code="401", error_msg="Unauthorized Access.", back_url="/")
        else:
            return render_template('success.html')

    if request.method == "POST":
        submitted = request.form.get("final_flag", "").strip()
        if submitted == FINAL_FLAG:
            session['authorized_win'] = True
            return redirect("/submit")
        else:
            return render_template('index.html', msg="INCORRECT FLAG COMBINATION.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006, debug=True)
