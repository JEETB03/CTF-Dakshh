import json
from flask import Flask, request, jsonify, render_template_string, make_response, redirect

app = Flask(__name__)
app.secret_key = 'hard_treasure_hunt_2026'

MEDIUM_FLAG_CONTENT = "css_gh0st_m3d1um"
HARD_FRAGMENT = "h4rd_fr4gm3nt_b0ss"
FINAL_FLAG = f"DAKSHH{{{MEDIUM_FLAG_CONTENT}_{HARD_FRAGMENT}}}"

INDEX_HTML = '''
<!DOCTYPE html>
<html>
<head><title>The Final Lock</title></head>
<body style="background: #000; color: #0f0; font-family: Courier New, Courier, monospace; text-align: center; margin-top: 50px;">
    <h1>The Turing Gate</h1>
    <p>Only humans can read the ancient runes to unlock the core.</p>
    
    <!-- Anti-AI Mechanisms: Inline SVG text rendering and spatial grouping -->
    <!-- LLMs analyzing this raw SVG code will struggle to extract the exact instructional sentence structure 
         because the text is broken into arbitrary tspan elements positioned relatively. -->
    <svg width="600" height="200" style="background: #111; border: 1px solid #0f0;">
        <text x="50" y="50" fill="#0f0" font-size="20">
            <tspan x="50" dy="0">OP</tspan>
            <tspan x="75" dy="0">TI</tspan>
            <tspan x="100" dy="0">ON</tspan>
            <tspan x="125" dy="0">S </tspan>
            
            <tspan x="200" dy="0">/a</tspan>
            <tspan x="230" dy="0">pi</tspan>
            <tspan x="260" dy="0">/co</tspan>
            <tspan x="290" dy="0">re</tspan>
        </text>
        <text x="50" y="100" fill="#0f0" font-size="20">
            <tspan x="50" dy="0">Th</tspan>
            <tspan x="75" dy="0">en</tspan>
            <tspan x="120" dy="0">P</tspan>
            <tspan x="140" dy="0">A</tspan>
            <tspan x="160" dy="0">TC</tspan>
            <tspan x="190" dy="0">H </tspan>
            <tspan x="220" dy="0">it</tspan>
            <tspan x="250" dy="0">...</tspan>
        </text>
        <text x="50" y="150" fill="#0f0" font-size="20">
            <tspan x="50" dy="0">Th</tspan>
            <tspan x="75" dy="0">en</tspan>
            <tspan x="120" dy="0">G</tspan>
            <tspan x="140" dy="0">E</tspan>
            <tspan x="160" dy="0">T </tspan>
            <tspan x="190" dy="0">th</tspan>
            <tspan x="220" dy="0">e </tspan>
            <tspan x="250" dy="0">Fr</tspan>
            <tspan x="270" dy="0">ag</tspan>
            <tspan x="290" dy="0">me</tspan>
            <tspan x="310" dy="0">nt.</tspan>
        </text>
    </svg>
    
    <br><br>
    <h2>Final Combine Terminal</h2>
    <p>Merge your Medium Flag content with the Hard Fragment to construct the True Flag.</p>
    <p>Format: <code>HITK{medium_content_hard_fragment}</code></p>
    
    <form action="/submit" method="POST">
        <input type="text" name="final_flag" placeholder="HITK{...}" size="50" style="padding: 10px; background:#222; color:#0f0; border:1px solid #0f0;">
        <button type="submit" style="padding: 10px; background:#0f0; color:#000; border:none; cursor:pointer;">Submit</button>
    </form>
    
    {% if msg %}
        <h3 style="color: red;">{{ msg }}</h3>
    {% endif %}
</body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return render_template_string(INDEX_HTML)

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

@app.route("/submit", methods=["POST"])
def submit():
    submitted = request.form.get("final_flag", "").strip()
    if submitted == FINAL_FLAG:
        return "<h1 style='color:green; text-align:center; margin-top:20%; font-family:monospace;'>ACCESS GRANTED: YOU HAVE FINISHED THE WEB TREASURE HUNT TRILOGY!</h1>"
    else:
        return render_template_string(INDEX_HTML, msg="INCORRECT FLAG COMBINATION.")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5006)
