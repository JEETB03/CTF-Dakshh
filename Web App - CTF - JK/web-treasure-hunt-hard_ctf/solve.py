import requests

BASE_URL = "http://127.0.0.1:5006"
session = requests.Session()

print("1. Sending OPTIONS request to /api/core...")
r1 = session.options(f"{BASE_URL}/api/core")
print("Response headers X-Configuration-Required:", r1.headers.get('X-Configuration-Required'))

print("\n2. Sending PATCH request to /api/core with JSON payload...")
r2 = session.patch(f"{BASE_URL}/api/core", json={"status": "ready"})
print("Response JSON:", r2.json())
print("Cookies received:", session.cookies.get_dict())

print("\n3. Sending GET request to /api/core...")
r3 = session.get(f"{BASE_URL}/api/core")
print("Response JSON:", r3.json())

hard_fragment = r3.json().get("fragment_value")
print(f"Extracted Hard Fragment: {hard_fragment}")

medium_content = "css_gh0st_m3d1um"
final_flag = f"DAKSHH{{{medium_content}_{hard_fragment}}}"
print(f"\nFinal Constructed Flag: {final_flag}")

print("\n4. Submitting final flag...")
r4 = session.post(f"{BASE_URL}/submit", data={"final_flag": final_flag})

if "ACCESS GRANTED" in r4.text:
    print("SUCCESS! Challenge completed.")
else:
    print("FAILED! Final submission rejected.")
