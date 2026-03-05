import requests

BASE_URL = "http://127.0.0.1:5005"
EASY_FLAG = "DAKSHH{h1nglish_hunt_3asy}"

print("1. Visiting /login with Easy Flag...")
session = requests.Session()
r1 = session.post(f"{BASE_URL}/login", data={"password": EASY_FLAG})
print("Did it redirect to stage1?", "stage1" in r1.url or "stage1" in r1.text)

print("\n2. Visiting Stage 1...")
r2 = session.get(f"{BASE_URL}/stage1")
print("Does stage1 have anti-bot fake flag?", "DAKSHH{th1s" in r2.text)

print("\n3. Following CSS ghost hint to /hidden_shadow...")
r3 = session.get(f"{BASE_URL}/hidden_shadow")
print("Is Stage 2 loaded?", "Shadow Realm" in r3.text)

print("\n4. Submitting password to vault...")
r4 = session.post(f"{BASE_URL}/vault", data={"passkey": "k3y_m4st3r_2026"})
print("Did vault unlock?", "vault" in r4.url)

print("\n5. Checking Vault contents...")
r5 = session.get(f"{BASE_URL}/vault")
if "DAKSHH{" in r5.text:
    print("SUCCESS! Found Medium Flag!")
    for line in r5.text.splitlines():
        if "DAKSHH" in line:
            print(line.strip())
else:
    print("FAILED! Flag not found.")
