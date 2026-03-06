# 🏴‍☠️ DAKSHH CTF – Challenges Repository

Welcome to the **DAKSHH CTF Challenge Series**. This repository contains a collection of custom-built challenges categorized by domain.

---

**Contributor:** JEET BISWAS

## 🌐 Web Exploitation Series

### Theme: *"The Web is a Lie."*

The **Polus Space Agency** has reported unusual behavior in several of their internal web systems. Logs indicate the presence of an unknown hacker group leaving cryptic references to hackers, vigilantes, pop stars, and… impostors. Your task is to investigate these web applications and recover the hidden flags.

Throughout the Web challenges, you will encounter subtle references to:
- 👨‍💻 **Mr. Robot**
- 🦇 **Batman / Wayne Enterprises**
- 🎶 **Alysa Liu – Stateside**
- 👨‍🚀 **Among Us**

**Challenges included:**
1. **Impostor in the DOM** (Easy) - Cross-Site Scripting (XSS)
2. **Wayne Enterprises Data Leak** (Easy/Medium) - Insecure Direct Object Reference (IDOR) via API
3. **Stateside Intercept** (Medium) - JWT Manipulation (`alg: none`)
4. **Mr. Robot's Archive Heist** (Hard) - Advanced Directory Traversal / LFI

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** JEET BISWAS

## 🔐 Crypto Challenge Series

Welcome to the **DAKSHH CTF Crypto Series**. These cryptography challenges focus on breaking realistic encryption implementations using thematic, pop-culture-inspired scenarios. 

Each challenge includes a player-facing `dist/` folder containing redacted source code and the exact output files.

**Challenges included:**
1. **Neo's Broken RNG** (Easy) - C++
    - *Theme*: The Matrix
    - *Concept*: Single-byte XOR key recovery via Known Plaintext Attack (KPA).
2. **Sherlock's Cipher Notebook** (Medium) - Java
    - *Theme*: Sherlock Holmes
    - *Concept*: Reused One-Time Pad (Many-Time Pad) vulnerability requiring crib-dragging.
3. **Cyberpunk Secure Broadcast** (Hard) - Python
    - *Theme*: Cyberpunk
    - *Concept*: RSA Broadcast Attack (Håstad's) exploiting a small public exponent ($e=3$).

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** Nabhonil Bhattacharjee

Welcome to the **DAKSHH CTF Reverse Engineering Series**. This section contains high-difficulty reverse engineering challenges designed to test your understanding of:

- Low-level program logic  
- LLVM IR analysis  
- XOR-based transformations  
- ASCII manipulation  
- Compiler-level thinking  

These are not brute-force challenges.  
They reward patience, structure, and deep reasoning.

**Challenges included:**
1. **Last Words of the Hacker** (Medium)
    - *Concept*: XOR-based transformations
2. **Are You Better Than Assembly?** (Hard)
    - *Concept*: LLVM IR / XOR / String manipulation

### 🛠 Recommended Tools
- Ghidra  
- IDA / Binary Ninja  
- clang (for compiling `.ll` files)  
- CyberChef  
- Python (for XOR analysis)  

### ⚠️ Rules
- No brute forcing.
- No patch-and-pray.
- No guessing flags.

Reverse it properly.

### 🧠 Final Advice
If you see:
- Static byte arrays  
- Suspicious modulo loops  
- XOR operations  
- Decoy output paths  

You’re on the right track.

Good luck.
*The compiler is watching.*

---

**Contributor:** Jyotirmoy Karmakar (0xjyotirmoy)

## 🌐 Web Exploitation Series (Extended)

These web challenges cover a wide spectrum of vulnerabilities — from classic SQL injection to advanced Anti-AI mechanisms designed to defeat automated scanners and LLMs. Each challenge includes detailed setup instructions, a step-by-step solving walkthrough, and an automated solve script for verification.

**Challenges included:**
1. **Authentication Bypass – Phantom Login** (Easy) - SQL Injection
    - *Concept*: Classic SQLi authentication bypass on a SQLite-backed login form.
2. **Blind SQL Injection – Advanced WAF Bypass** (Medium) [*Anti-AI*]
    - *Concept*: Blind SQLi via `ORDER BY` + `INSTR()` function to extract data while evading a keyword-based WAF.
3. **SQL Injection – Unicode Phantom** (Hard) [*Anti-AI*]
    - *Concept*: Unicode Normalization (`NFKC`) bypass — fullwidth apostrophe `＇` passes WAF, then normalizes to `'` on the backend.
4. **Web Treasure Hunt** (Easy) [*Anti-AI*]
    - *Concept*: Hinglish-hint reconnaissance with fake flag traps, Base64 decoding, and command injection.
5. **Web Treasure Hunt – CSS Ghost** (Medium) [*Anti-AI*]
    - *Concept*: All hints rendered via CSS `::after` pseudo-elements — invisible to `curl` and DOM scrapers.
6. **Web Treasure Hunt – Turing Test API** (Hard) [*Anti-AI*]
    - *Concept*: SVG-obfuscated instructions leading to a strict `OPTIONS → PATCH → GET` API sequence with state-dependent cookies.
7. **Reflective XSS Cookie Steal** (Medium)
    - *Concept*: WAF bypass using `<svg/onload=...>`, Puppeteer admin bot simulation, cookie exfiltration.
8. **Host Header Injection** (Medium)
    - *Concept*: Password Reset Poisoning via spoofed `Host` header to steal admin reset tokens.

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** Jyotirmoy Karmakar (0xjyotirmoy)

## 🔐 Crypto Challenge Series (Extended)

**Challenges included:**
1. **Quantum Steps** (Medium) - Python
    - *Theme*: Discrete Logarithm
    - *Concept*: Baby-step Giant-step algorithm to solve a DLP and recover the AES decryption key for the encrypted flag.

All flags follow the format: `DAKSHH{example_flag_here}`

---

**Contributor:** Antigravity

## 🕵️‍♂️ Misc Challenges

Cyberpunk hacker-themed narrative challenges involving various data analysis skills.

**Challenges included:**
1. **The Last Beacon** (Easy)
    - *Theme*: Morse Code / Signal Analysis
2. **Glitched Identity** (Easy)
    - *Theme*: QR Code Recovery / Error Correction
3. **Poisoned Intelligence** (Medium)
    - *Theme*: AI Data Poisoning / Dataset Inspection

These unique challenges have an alternative flag format: `flag{example_flag_here}`
