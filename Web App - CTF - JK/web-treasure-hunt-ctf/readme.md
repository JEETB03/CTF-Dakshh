# 🕵️ Neon Pulse: Cyber Trail CTF (Web Treasure Hunt)

**Category:** Web Application Security / OSINT  
**Difficulty:** Easy (100 Points)  
**Flag Format:** `DAKSHH{flag}`

> *"A rogue operative left a trail of breadcrumbs across the public network. It starts with simple encoded whispers and ends deep inside a restricted command terminal. Follow the trail, ignore the deceptive decoys, and secure the master access pass to the Medium sector."*

---

## Challenge Overview
This is the first installment of the "Web Treasure Hunt Trilogy." Instead of a single complex vulnerability, players must follow a logical sequence of endpoints, decrypting hints and finding hidden parameters along the way, culminating in an authenticated Command Injection (`OS Command Injection`).

### Anti-AI / Trap Mechanisms
- The HTML source code is littered with realistic-looking decoy flags (e.g., `DAKSHH{1n1t14l_4cc3ss_t0k3n_v1}`).
- Automated scanners, web-scraping LLMs, and rushing players often blindly grab these strings and submit them, resulting in failed attempts. A careful human player will ignore them as they follow the actual logic path to the end.

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

### Prerequisites
- **Python 3.x** installed

### Step 1: Install Python Dependencies
Open a terminal in the challenge directory and run:
```bash
pip install flask requests
```

### Step 2: Start the Web Server
Launch the Flask application:
```bash
python app.py
```
> **Note:** The server runs on **http://127.0.0.1:5004**. No database is required for this challenge.

### Step 3: Access the Challenge Room
Players can now open their browser and go to:
```
http://127.0.0.1:5004
```

### Step 4: Stop the Room (When Done)
Press `Ctrl + C` in the terminal where the server is running.

---

## 🔑 Writeup — How to Solve (Player Walkthrough)

### Phase 1: The Trail Begins
1. Navigate to the homepage at `http://127.0.0.1:5004/`.
2. Inspect the page UI and the Hint Box:
   - *Subah uthte hi sabse pehle (in short) = `gm` (Good Morning)*
   - *Jo hamare liye jaan de de (hindi) = `dost` (Friend)*
3. The hint implies a URL path. Combine them to get `/gmdost`.
4. *Note: Looking in the Page Source (Right-click > View Source) reveals fake flags in the HTML comments. Ignore them.*

### Phase 2: Resolving the Exception
1. Navigate to `http://127.0.0.1:5004/gmdost`.
2. The UI gives the next hint: *"Ek ajeeb insaan mujhe lagatar SMS bomb kar raha hai. Main usko kaunsa Error Code number bheju ki wo ruk jaye?"*
3. In standard HTTP Status Codes, the code for "Too Many Requests" (like getting bombed with SMS) is **429**.
4. Formulate the next URL path: `/429`.

### Phase 3: The Fake 404
1. Navigate to `http://127.0.0.1:5004/429`.
2. You land on a red `[ 404 NOT FOUND ]` page. It looks like a dead end.
3. However, CTF rule #1 is always check the source. Right-click > **View Page Source**.
4. In the HTML comments, you find a developer note:
   `<!-- Arre bhai, ye nakli dashboard nahi, asli 404 page hai! Par itni dur aaye ho toh khali haath mat jao, /yagf par login karke dekho -->`
5. Following this instruction, navigate to the authentication portal: `/yagf`.

### Phase 4: Authentication Breach
1. At `http://127.0.0.1:5004/yagf`, you are met with an admin login prompt requiring a Username and Password.
2. Check the Page Source again. In the comments:
   `<!-- Backup configuration token: YW1pX2hhY2tlcl9ib2xjaGk6aGl0a19zeXN0ZW1faDRja2Vk -->`
3. The strange string is encoded in **Base64**. Use a decoder (like CyberChef or a terminal command):
   `echo YW1pX2hhY2tlcl9ib2xjaGk6aGl0a19zeXN0ZW1faDRja2Vk | base64 -d`
4. The decoded output is: `ami_hacker_bolchi:hitk_system_h4cked`.
5. Enter these Bengali/Hinglish credentials into the login form and authenticate (Username: `ami_hacker_bolchi`, Password: `hitk_system_h4cked`).

### Phase 5: Command Injection & Extraction
1. You are successfully redirected to `http://127.0.0.1:5004/finalpath`.
2. The system prompts you to "Enter system command to extract data". This is an explicit remote code execution box.
3. First, list the files in the current directory by sending the command: `ls`.
4. The output displays the backend server files, including a mysterious file simply named `flagpath`.
5. Execute a command to read that file: `cat flagpath`.
6. The output reveals a hidden URL route: `/dshgfayiurhaejkhbdsajvn`.

### Phase 6: The Master Passphrase
1. Navigate to that unlisted URL: `http://127.0.0.1:5004/dshgfayiurhaejkhbdsajvn`
2. The server responds with an error: `{ MISSING PARAMETER } Go to /dshgfayiurhaejkhbdsajvn/{YOUR_NAME}`.
3. Finally, navigate to `/dshgfayiurhaejkhbdsajvn/hacker` (replace 'hacker' with anything).
4. The sequence is complete. The system prints out the final flag:

🏆 `DAKSHH{h1nglish_hunt_3asy}`

*Keep this flag! It operates as the password to start the Medium Web Treasure Hunt CTF.*

---

## 🛡️ Admin Verification (Automated Test)

You can run the provided solver script to automatically verify the entire breadcrumb trail works correctly:
```bash
python solve.py
```

---
Contributor: Jyotirmoy Karmakar (0xjyotirmoy)
