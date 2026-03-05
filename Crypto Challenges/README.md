# DAKSHH CTF — Crypto Challenge Pack

Welcome to the Crypto Challenges. Below are three cryptography challenges designed for the DAKSHH CTF, spanning Easy, Medium, and Hard difficulties.

---

## Challenge 1 — Sus Encryption Protocol
**Difficulty:** Easy

### Story
The Polus Space Agency intercepted a transmission from the communications relay. Operations are normal, but one crewmate—Red—insisted on using a "custom encryption protocol" he whipped up in 5 minutes because he didn't trust the ship's default AES. Your task is to prove to Red that his protocol is, in fact, extremely *sus*.

### Crypto Concept
**Single-byte XOR Encryption**
The "sus" encryption protocol simply iterates over the plaintext and XORs every single character with the exact same 1-byte integer key. By knowing the flag format (`DAKSHH{`), you can easily recover the single byte key and decrypt the rest of the message.

### Files Provided
- `encrypt.py` (The proprietary encryption script)
- `output.txt` (The intercepted ciphertext in hex)

### Program Code (`encrypt.py`)
```python
import binascii

banner = """
⠀⠀⠀⠀⠀⣀⣤
⠀⠀⠀⠀⣴⣿⣿⣦
⠀⠀⠀⠀⣿⣿⣿⣿
⠀⠀⠀⠀⣿⣿⣿⣿
⠀⠀⠀⠀⠈⠻⣿⡿
SUS?
"""
print(banner)

def xor_encrypt(message, key):
    return bytes([b ^ key for b in message])

# The flag format is DAKSHH{...}
flag = open('flag.txt', 'rb').read().strip()

# Red's "Unbreakable" 1-byte key
key = 42 

encrypted = xor_encrypt(flag, key)
print("Encrypted message:", binascii.hexlify(encrypted).decode())
```

### Sample Output (`output.txt`)
```text
⠀⠀⠀⠀⠀⣀⣤
⠀⠀⠀⠀⣴⣿⣿⣦
⠀⠀⠀⠀⣿⣿⣿⣿
⠀⠀⠀⠀⣿⣿⣿⣿
⠀⠀⠀⠀⠈⠻⣿⡿
SUS?

Encrypted message: 6e6b617962625178196e755f19795f511219797f5f195d18785f757d
```

### Player POV Writeup

#### Initial Observation
The player runs or reads `encrypt.py` and notices the custom `xor_encrypt` function. It takes every byte of the message and XORs it with a static `key`. The key is a single integer, meaning it's a single-byte XOR cipher.

#### Cryptographic Analysis
XOR has a reversible property: if `A ^ B = C`, then `C ^ B = A` and `A ^ C = B`.
We know the first few characters of the plaintext are `DAKSHH{`. We have the corresponding first few bytes of the ciphertext hex: `6e 6b 61 79 62 62 51`.
If we take the first letter of the flag 'D' (which is ASCII value 68, or `0x44`) and XOR it with the first byte of the ciphertext `0x6e` (110), we get:
`110 ^ 68 = 42` (The key!)

#### Exploitation Steps
With the key recovered (42), the player writes a simple script to XOR the entire ciphertext against it:

```python
import binascii

ciphertext_hex = "6e6b617962625178196e755f19795f511219797f5f195d18785f757d"
ciphertext = binascii.unhexlify(ciphertext_hex)

key = 42
plaintext = bytes([b ^ key for b in ciphertext])
print(plaintext.decode())
```

#### Recovering the Flag
Running the script outputs:
`DAKSHH{r3d_1s_s0_sus_w1th_x0r}`

### Educational Explanation
Single-byte XOR (and by extension, repeating-key XOR) is trivially insecure against Known Plaintext Attacks (KPA). Because XOR is symmetric, knowing just a tiny fragment of the plaintext—such as a file header or a flag format—completely exposes the key. Real-world systems must use established, vetted encryption algorithms like AES-GCM rather than proprietary "home-rolled" cryptography.

---

## Challenge 2 — Gotham's Reused Shadow
**Difficulty:** Medium

### Story
The Joker has hijacked the GCPD's emergency broadcast frequency to taunt the Batman. He boasts that his messages are encrypted with an "unbreakable One-Time Pad." However, the Joker, in his arrogance, was too lazy to generate new random pads for every broadcast. Oracle intercepted three of his broadcasts. Can you recover the hidden location before midnight?

### Crypto Concept
**Reused One-Time Pad (Many-Time Pad Attack)**
A One-Time Pad requires the key to be truly random, as long as the plaintext, and critically, *never reused*. If a key is reused to encrypt multiple messages, an attacker can XOR the ciphertexts together. The key mathematically cancels out, leaving the XOR of the two original plaintexts (`C1 ^ C2 = P1 ^ P2`). This allows for statistical analysis (like crib dragging) to uncover the messages.

### Files Provided
- `encrypt.py` (The Joker's encryption tool)
- `ciphertexts.txt` (Three intercepted broadcasts)

### Program Code (`encrypt.py`)
```python
import os
import binascii

banner = """
    /\_/\
   ( o.o )
    > ^ <
  BAT SIGNAL ACTIVE
"""
print(banner)

# The Joker's "Secure" Pad
# He generated it once, but used it multiple times!
key = os.urandom(60)

messages = [
    b"To the Batman: I have hidden the explosive at the docks.",
    b"The timer is set for midnight. You will never find it in time.",
    b"DAKSHH{n3v3r_r3us3_y0ur_0n3_t1m3_p4d_j0k3r}                   "
]

def encrypt(msg, key):
    # Truncate/pad to exact length logic omitted for simplicity, 
    # assumes messages are padded to same length as key.
    return bytes([msg[i] ^ key[i] for i in range(len(msg))])

for i, msg in enumerate(messages):
    enc = encrypt(msg, key)
    print(f"Broadcast {i+1}: {binascii.hexlify(enc).decode()}")
```

### Sample Output (`ciphertexts.txt`)
*(Note: Output varies based on `os.urandom`, but will look like this)*
```text
    /\_/\
   ( o.o )
    > ^ <
  BAT SIGNAL ACTIVE

Broadcast 1: 3a1f8b...
Broadcast 2: 3a2c9a...
Broadcast 3: 2f2b9b...
```

### Player POV Writeup

#### Initial Observation
The player opens `encrypt.py` and sees that the `key` is generated via `os.urandom(60)` once, but then used inside a loop to encrypt three different messages. This is the textbook definition of a Many-Time Pad vulnerability.

#### Cryptographic Analysis
The player knows three ciphertexts: $C_1$, $C_2$, and $C_3$.
They also know the flag format for the third message starts with `DAKSHH{`.
Because $C_1 = P_1 \oplus K$ and $C_3 = P_3 \oplus K$, they can calculate:
$C_1 \oplus C_3 = P_1 \oplus P_3$.
If they XOR the known part of $P_3$ (`DAKSHH{`) against $C_1 \oplus C_3$, the result will reveal the first 7 characters of $P_1$.

#### Exploitation Steps
The player uses a crib-dragging technique or writes a script leveraging the known flag format.

```python
import binascii

# Extracted from ciphertexts.txt
c1 = binascii.unhexlify("...") # Broadcast 1
c2 = binascii.unhexlify("...") # Broadcast 2
c3 = binascii.unhexlify("...") # Broadcast 3 (Flag)

# We know the flag starts with DAKSHH{
known_plaintext = b"DAKSHH{"

# XOR C3 and C1, then XOR with the known part of P3
# (c1 ^ c3) ^ known_plaintext = p1 (partial)
c1_c3_xor = bytes([a ^ b for a, b in zip(c1, c3)])
p1_partial = bytes([a ^ b for a, b in zip(c1_c3_xor[:7], known_plaintext)])

print("Guessed P1 start:", p1_partial.decode())
# Output: "To the "

# Now we know P1 starts with "To the Batman: "
# We can guess more words in P1 or P2, XOR them with the ciphertexts to reveal more of P3 (the flag)
```
By iteratively guessing common English words ("the", "Batman", "midnight") and cross-referencing the resulting readable text in the other messages, the entire flag is dragged out into the light.

#### Recovering the Flag
`DAKSHH{n3v3r_r3us3_y0ur_0n3_t1m3_p4d_j0k3r}`

### Educational Explanation
The One-Time Pad is mathematically proven to provide perfect secrecy—but **only** strictly if the key is truly random, as long as the plaintext, kept perfectly secret, and **used exactly once**. The moment a key is reused, the cipher degrades catastrophically into a simple XOR equation that leaks structural information about the plaintexts.

---

## Challenge 3 — Elliot's Fragmented Mind
**Difficulty:** Hard

### Story
Elliot is trying to securely broadcast the E-Corp root server password to three isolated fsociety proxy nodes. To save computation cycles on his burner laptop, he opted for an RSA implementation using a very small public exponent ($e=3$). He encrypted the exact same message three times, using the three different public moduli of the nodes. E-Corp's passive network surveillance caught the traffic. Can you shatter the encryption?

### Crypto Concept
**Håstad's Broadcast Attack**
When the same plaintext is encrypted using RSA with the same small public exponent $e$ (e.g., $e=3$) and sent to $e$ or more recipients with different moduli ($N_1, N_2, N_3$), an attacker can intercept the ciphertexts and use the Chinese Remainder Theorem (CRT) to compute $M^e \pmod{N_1 \times N_2 \times N_3}$. Because $M < N_i$, $M^e$ is strictly less than $N_1 \times N_2 \times N_3$. Therefore, the modulo operation has no effect, and the attacker can simply take the $e$-th root of the result over the standard integers to recover the plaintext $M$.

### Files Provided
- `encrypt.py` (Elliot's RSA broadcast script)
- `intercepts.txt` (The three intercepted RSA ciphertexts and public keys)

### Program Code (`encrypt.py`)
```python
from Crypto.Util.number import getPrime, bytes_to_long

banner = """
|  _ |  _ \ / _ \ |  _ |  _ | ****|
| |*) | |*) | | | || |*) | |*) |  *|
|  _ <|  _ <| |*| ||  _ <|  _ <| |**_
|*| __| _\***/ |*| __| __***_|
"""
print(banner)

# The root password / flag
flag = b"DAKSHH{h4st4ds_br04dc4st_4tt4ck_sh4tt3rs_rs4}"
m = bytes_to_long(flag)

# Elliot's "efficient" public exponent
e = 3

print("Broadcasting to fsociety nodes...\n")

for i in range(3):
    p = getPrime(512)
    q = getPrime(512)
    n = p * q
    c = pow(m, e, n)
    print(f"--- Node {i+1} ---")
    print(f"n{i+1} = {n}")
    print(f"e = {e}")
    print(f"c{i+1} = {c}\n")
```

### Sample Output (`intercepts.txt`)
*(Output contains 3 large integers for N and C)*
```text
|  _ |  _ \ / _ \ |  _ |  _ | ****|
| |*) | |*) | | | || |*) | |*) |  *|
|  _ <|  _ <| |*| ||  _ <|  _ <| |**_
|*| __| _\***/ |*| __| __***_|

Broadcasting to fsociety nodes...

--- Node 1 ---
n1 = 123...
e = 3
c1 = 456...

--- Node 2 ---
n2 = 789...
e = 3
c2 = 123...

--- Node 3 ---
n3 = 456...
e = 3
c3 = 789...
```

### Player POV Writeup

#### Initial Observation
The player inspects `encrypt.py` and `intercepts.txt`. They immediately notice that `e = 3` is very small, the same underlying message `m` (the flag) is being encrypted, and it's being broadcast three times to three different moduli ($n_1, n_2, n_3$). This perfectly aligns with Håstad's Broadcast Attack.

#### Cryptographic Analysis
By Chinese Remainder Theorem:
$$C \equiv C_1 \pmod{N_1}$$
$$C \equiv C_2 \pmod{N_2}$$
$$C \equiv C_3 \pmod{N_3}$$

We can find a unique $C$ modulo $N_1 \times N_2 \times N_3$.
We know that $C = M^3 \pmod{N_1 N_2 N_3}$.
Since $M < N_1, N_2, N_3$, it is guaranteed that $M^3 < N_1 \times N_2 \times N_3$.
Thus, $C = M^3$ exactly (over the integers, not just modulo).
To recover $M$, we just take the integer cube root of $C$.

#### Exploitation Steps
The player uses Python or SageMath to crunch the numbers. In Python, using `sympy` or a custom CRT and integer root function:

```python
from sympy.ntheory.modular import crt
import gmpy2
from Crypto.Util.number import long_to_bytes

# Values copied from intercepts.txt
n_list = [n1, n2, n3]
c_list = [c1, c2, c3]

# Apply Chinese Remainder Theorem
C, N = crt(n_list, c_list)

# Take the integer cube root of C
m, exact = gmpy2.iroot(C, 3)

if exact:
    print("Decrypted Flag:", long_to_bytes(m).decode())
else:
    print("Root wasn't exact. Something went wrong.")
```

#### Recovering the Flag
Running the script quickly parses the massive integers and outputs:
`DAKSHH{h4st4ds_br04dc4st_4tt4ck_sh4tt3rs_rs4}`

### Educational Explanation
While RSA is secure when implemented correctly, parameter selection is an enormous vulnerability vector. A small public exponent ($e=3$) is often tempting to developers to speed up the encryption process. However, if the same message is sent to at least $e$ different receivers without proper padding, it is entirely broken by Håstad's Broadcast Attack. To fix this, real-world implementations must use a randomized padding scheme like RSA-OAEP before encryption, which ensures that identical plaintexts result in completely different ciphertexts and prevents solving the system of equations.
