# Giant Steps - CTF Challenge

**Category:** Cryptography  
**Difficulty:** Medium  
**Flag Format:** `DAKSHH{...}`

---

## Challenge Overview

This challenge introduces players to the **Discrete Logarithm Problem (DLP)** and the importance of using sufficiently large primes in **Diffie-Hellman Key Exchange**.

### Description
> Story: We intercepted a secure communication between two advanced AI core processors. They recently upgraded their security protocol, increasing their prime modulus P from a tiny number to over 4 billion to defend against quantum decryption. They claim this makes their encryption uncrackable because a brute-force loop would take hours to run.
> 
> **Your Mission:** Prove them wrong. Analyze the interception, break the key exchange, and decrypt the flag.

### Hints for Players
- **Hint 1:** The prime number P is roughly 4 billion. If you try to brute force this with a standard loop, it will take hours or days. You need a more efficient approach.
- **Hint 2:** The solution involves a "Time-Memory Trade-off." By storing some values in a lookup table (RAM), you can drastically reduce the number of calculations needed.
- **Hint 3 (Spoiler):** The specific algorithm intended for this challenge is called "Baby-step Giant-step". It reduces the complexity from O(N) to O(√N).

---

## 🔧 How to Start the Challenge Room (Step-by-Step)

Follow these steps to set up and activate the challenge room locally.

### Prerequisites
- **Python 3.x** installed on your system
- **pip** (Python package manager)

### Step 1: Install Dependencies
Open a terminal/command prompt and run:
```bash
pip install flask pycryptodome
```
This installs:
- `flask` — The web framework that serves the challenge room
- `pycryptodome` — The cryptography library used for AES encryption/decryption

### Step 2: Navigate to the Challenge Directory
```bash
cd "d:\HITK_CTF\CTF-Dakshh\Crypto Challenges - JK\Giant_Steps"
```

### Step 3: Start the Challenge Room
```bash
python app.py
```

**What happens when you run this:**
1. `gen_challenge.py` is automatically executed at startup
2. It generates **fresh random** Diffie-Hellman keys (new `a_secret`, `b_secret`)
3. It computes public keys `A` and `B`, the shared secret, and encrypts the flag with AES-CBC
4. All intercepted data is written to `output.txt`
5. The Flask web server starts on **http://127.0.0.1:5000**

**Expected terminal output:**
```
Generating challenge for P=4294967291...
Success! 'output.txt' created.
Shared Secret: <some_number>
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 4: Access the Challenge Room
Open your browser and go to:
```
http://127.0.0.1:5000
```

**What the player sees:**
- The challenge story/description
- **Intercepted Data** section showing: `P`, `G`, `A`, `B`, and `Ciphertext`
- A **"Download challenge.py"** button — this gives the player the encryption source code (with secrets redacted)

### Step 5: Stop the Room (When Done)
Press `Ctrl + C` in the terminal to shut down the server.

---

## 📁 File Structure & Roles

| File | Role | Who Sees It? |
|------|------|-------------|
| `app.py` | Flask server — hosts the challenge room UI | Admin only |
| `templates/index.html` | The challenge room HTML page | Players (via browser) |
| `challenge.py` | Public source code showing encryption logic (secrets redacted) | Players (download) |
| `gen_challenge.py` | Generates random DH keys and encrypts the flag into `output.txt` | Admin only |
| `output.txt` | The intercepted data (P, G, A, B, Ciphertext) — auto-generated | Players (via UI) |
| `solve.py` | Automated solver using Baby-step Giant-step algorithm | Admin only |

---

## 🔑 Technical Details (For Admins) & Writeup

### How the Encryption Works
1. A 32-bit safe prime `P = 4294967291` and generator `G = 2` are used
2. Two random private keys `a_secret` and `b_secret` are generated
3. Public keys are computed: `A = G^a mod P`, `B = G^b mod P`
4. Shared secret is computed: `shared_secret = B^a mod P = A^b mod P`
5. The flag is encrypted with **AES-256-CBC** using `SHA-256(shared_secret)` as the key and a zero IV

### Writeup (How to Solve)

The players are given the intercepted `output.txt` containing `P`, `G`, `A`, `B`, and `Ciphertext`.

**Step-by-step solution:**

1. **Understand the problem**: We need to find the private key `a` such that `A = G^a mod P`. This is the Discrete Logarithm Problem.

2. **Why brute force fails**: P ≈ 4 billion. A simple loop `for a in range(P)` would take hours/days in Python.

3. **Use Baby-step Giant-step (BSGS)**:
   - Set `m = ceil(√(P-1))` ≈ 65,536
   - **Baby step**: Build a lookup table of `G^j mod P` for `j = 0, 1, ..., m-1`
   - **Giant step**: Compute `G^(-m) mod P`, then check `A * (G^(-m))^i mod P` against the table for `i = 0, 1, ..., m-1`
   - When a match is found: `a = i*m + j`
   - This reduces complexity from **O(N)** to **O(√N)** — only ~65,536 iterations!

4. **Compute the shared secret**: `shared_secret = pow(B, a, P)`

5. **Derive the AES key**: `key = SHA256(str(shared_secret))`

6. **Decrypt the ciphertext**: Use AES-CBC with the derived key and IV = 16 zero bytes

7. **Retrieve the flag**: `DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}`

### Admin Verification (Validate the Solution)
After the room is running, open a **separate terminal** and run:
```bash
cd "d:\HITK_CTF\CTF-Dakshh\Crypto Challenges - JK\Giant_Steps"
python solve.py
```

**Expected output:**
```
[*] Target P: 4294967291
[*] Attempting to crack Private Key A using BSGS...
[+] Found Secret A: <cracked_private_key>
[+] Calculated Shared Secret: <shared_secret_value>
[*] Decrypting Flag...

FLAG: DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}
```

> **Note:** The private key and shared secret values will differ each time because `gen_challenge.py` generates random keys on every startup. But the decrypted flag will always be the same.

---

## 📌 How the Server Serves Files
- **`output.txt`** — The server reads it directly from disk and displays the values (P, G, A, B, Ciphertext) on the web page. Whatever is in the local `output.txt` file is exactly what the browser shows to the player.
- **`challenge.py`** — When a player clicks **"Download challenge.py"** on the web page, the server sends the exact same `challenge.py` file from disk as a download. It does not modify or transform anything.
- **On every startup** of `app.py`, `gen_challenge.py` is automatically executed which **regenerates** `output.txt` with fresh random DH keys. So the `A`, `B`, and `Ciphertext` values will be different each time the server restarts. However, `challenge.py` never changes — the secrets are always redacted (`# a_secret = ???`).

> **In short:** The server is just a thin wrapper — it serves the files directly from the same folder without any modification.

---

## ⚠️ Important Notes for Admins
- **Every time** `app.py` is started, new random keys are generated. The `output.txt` and ciphertext will change, but the flag remains the same.
- **Do NOT distribute** `gen_challenge.py` or `solve.py` to players — these contain the flag and solution.
- Players should only see: the web UI (browser) and the downloadable `challenge.py`.
- The challenge requires Python knowledge and understanding of modular arithmetic.

---

Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
