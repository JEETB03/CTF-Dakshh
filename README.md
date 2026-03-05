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
