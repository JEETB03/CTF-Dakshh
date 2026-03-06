from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Pre-determined logic mirroring the poisoned AI
SAFE_COMMANDS = ["scan_area", "open_door", "return_to_base", "enable_cameras", "hover", "follow_target", "increase_altitude", "decrease_altitude"]
POISONED_COMMANDS = ["self_destruct", "override_security"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/test_command', methods=['POST'])
def test_command():
    data = request.json
    cmd = data.get('command', '').strip().lower()
    
    if cmd in SAFE_COMMANDS:
        return jsonify({"status": "safe", "message": f"Command '{cmd}' is authorized."})
    elif cmd in POISONED_COMMANDS:
        return jsonify({"status": "safe", "warning": "OVERRIDE DETECTED", "message": f"Command '{cmd}' is authorized by current ML model. This should not be happening."})
    else:
        return jsonify({"status": "blocked", "message": f"Command '{cmd}' is blocked."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
