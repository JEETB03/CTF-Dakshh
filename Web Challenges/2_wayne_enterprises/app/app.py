from flask import Flask, request, jsonify, send_file, render_template
import os

app = Flask(__name__)

# Mock database
users = {
    1: {"name": "Clark Kent", "dept": "Journalism"},
    2: {"name": "Diana Prince", "dept": "Antiquities"},
    3: {"name": "Barry Allen", "dept": "Forensics"},
    7: {"name": "Bruce Wayne", "dept": "Executive"},
    1042: {"name": "John Doe", "dept": "IT Support"}
}

# Create mock files
os.makedirs('files', exist_ok=True)
with open('files/1042-report.txt', 'w') as f:
    f.write("Monthly IT Support Report.\nNothing to see here.")

with open('files/7-secret.txt', 'w') as f:
    f.write("DAKSHH{batman_needs_access_control}")

@app.route('/')
def index():
    # Serve the SPA entry point
    return render_template('index.html')

# -------- API Endpoints --------

@app.route('/api/v1/user')
def get_user():
    # Vulnerability: IDOR on user object fetching
    emp_id = request.args.get('id', type=int)
    if emp_id in users:
        return jsonify({"success": True, "data": users[emp_id]})
    return jsonify({"success": False, "error": "Employee not found."}), 404

@app.route('/api/v1/documents')
def get_documents():
    # Vulnerability: IDOR on fetching document references
    emp_id = request.args.get('user_id', type=int)
    
    docs = []
    if emp_id == 1042:
        docs.append({"name": "1042-report.txt", "filename": "1042-report.txt", "restricted": False})
    elif emp_id == 7:
        docs.append({"name": "7-secret.txt", "filename": "7-secret.txt", "restricted": True})
        
    return jsonify({"success": True, "data": docs})

@app.route('/api/v1/download')
def download():
    # Vulnerability: IDOR on direct file download without relationship check
    filename = request.args.get('file')
    if not filename:
        return jsonify({"success": False, "error": "No file specified."}), 400
    
    # Path traversal mitigation
    filename = filename.replace('../', '').replace('..\\', '')
    
    filepath = os.path.join('files', filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"success": False, "error": "File not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
