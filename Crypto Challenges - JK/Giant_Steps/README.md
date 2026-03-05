# Quantum Steps - CTF Challenge

**Category:** Cryptography
**Difficulty:** Medium

## Challenge Overview

This challenge introduces players to the **Discrete Logarithm Problem (DLP)** and the importance of using sufficiently large primes in Diffie-Hellman Key Exchange.

### Description
> Story: We intercepted a secure communication between two advanced AI core processors. They recently upgraded their security protocol, increasing their prime modulus P from a tiny number to over 4 billion to defend against quantum decryption. They claim this makes their encryption uncrackable because a brute-force loop would take hours to run.
> 
> **Your Mission:** Prove them wrong. Analyze the interception, break the key exchange, and decrypt the flag.

- **Objective:** Recover the flag encrypted with AES. The encryption key is derived from the Diffie-Hellman shared secret.
- **Hint 1:** The prime number P is roughly 4 billion. If you try to brute force this with a standard loop, it will take hours or days. You need a more efficient approach.
- **Hint 2:** The solution involves a "Time-Memory Trade-off." By storing some values in a lookup table (RAM), you can drastically reduce the number of calculations needed.
- **Hint 3 (Spoiler):** The specific algorithm intended for this challenge is called "Baby-step Giant-step". It reduces the complexity from O(N) to O(sqrt(N)).

---

## Technical Details (For Admins) & Writeup

### Writeup (How to Solve)
The players are given `output.txt` which contains the prime **P**, base **G**, and public keys **A** and **B**, as well as the encrypted flag (AES-CBC encrypted using the SHA-256 hash of the shared secret).
Because the modulus **P** is around 4 billion (\(2^{32}\)), a simple brute-force of \(A = G^a \pmod P\) to find the secret exponent \(a\) takes too long in Python.
However, using the **Baby-step Giant-step** algorithm, the time complexity is reduced to \(O(\sqrt{P})\), which is around 65,536 iterations. 
1. The solver must implement Baby-step Giant-step to recover the private key `A`.
2. Compute the shared secret: `shared_secret = pow(B, a, P)`.
3. Hash the shared secret with SHA-256 to get the AES key.
4. Decrypt the `Ciphertext` using standard AES-CBC to retrieve the flag `DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}`.

### Room Setup / Admin Instructions
- **`app.py`**: A Flask server that hosts the challenge description, intercepts `output.txt` dynamically, and allows the player to download `challenge.py`.
- **`challenge.py`**: The *public* source code given to players. It shows the encryption logic but has the secret keys redacted.
- **`gen_challenge.py`**: (Admin Only) The script used to generate the keys, intercepts, and encrypted flag. On running, outputs the randomized data to `output.txt`. **Do not distribute directly.**
- **`solve.py`**: (Admin Only) An automated solver script that cracks the challenge using the Baby-step Giant-step algorithm.

#### Deployment & Verification
1. Ensure you have Python with `flask` and `pycryptodome` installed (`pip install flask pycryptodome`).
2. Start the web application:
   ```bash
   python app.py
   ```
   *Note: This automatically runs `gen_challenge.py` at startup to create fresh keys in `output.txt`.*
3. Validate the solution using the intended exploit logic:
   ```bash
   python solve.py
   ```

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
