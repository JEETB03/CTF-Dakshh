# Cyberpunk Secure Broadcast - Writeup

**Difficulty:** Hard
**Flag:** `DAKSHH{n0_c0rp0_n3tw0rk_1s_s4f3_fr0m_rs4}`

## CTFd Room Description
> "Burn corpo trash."
> 
> A rogue, sub-dermal AI operating in the shadows of Night City is continuously broadcasting rotating root keys to three isolated corporate databanks. To dodge Arasaka's NetRunners and preserve processing cycles on its burner rig, the AI is taking massive mathematical shortcuts with its RSA implementation.
> 
> We've jacked into the mainline and captured the Python script it's using, along with the raw packets containing the moduli and ciphertexts for all three databanks. The encryption algorithm is technically RSA, but a severe implementation flaw leaves it wide open. Shatter the encryption, zero out the math, and retrieve the root key before their ICE traces us back.

## Initial Recon
Players receive `encrypt.py` and `intercepts.txt`. Looking at the Python script, we observe an RSA encryption scheme. The `flag` is converted to a long integer `m`. We notice that the public exponent `e` is extremely small: `e = 3`. 
Crucially, the exact same message `m` is generated three times using the `pow(m, e, n)` function against three purely random moduli (`n1`, `n2`, `n3`). This is the classic setup for **Håstad's Broadcast Attack**.

## Cryptographic Analysis
By Chinese Remainder Theorem (CRT), if we have the same message $M$ encrypted to $e$ or more recipients with different moduli $N_i$:
$$C_1 \equiv M^3 \pmod{N_1}$$
$$C_2 \equiv M^3 \pmod{N_2}$$
$$C_3 \equiv M^3 \pmod{N_3}$$

We use the CRT to find a unique integer $C$ modulo $N_{total}$ (where $N_{total} = N_1 \times N_2 \times N_3$).
Because the message $M$ is strictly less than each $N_i$, it is guaranteed that $M^3 < N_1 \times N_2 \times N_3$.
Therefore, the modulo operation has absolutely no wrapping effect. We can simply calculate the actual integer cube root of $C$ over the standard integers to recover $M$.

## Exploitation Steps
We can write a Python script leveraging `sympy` (for CRT) and `gmpy2` or custom binary search (for integer roots) to piece the flag back together.

```python
from sympy.ntheory.modular import crt
import gmpy2
from Crypto.Util.number import long_to_bytes

# Paste these values from intercepts.txt
n_list = [
    # N1 here, N2 here, N3 here
]
c_list = [
    # C1 here, C2 here, C3 here
]

# Apply Chinese Remainder Theorem
# Returns C and N_total (we only care about C)
C, N_total = crt(n_list, c_list)

# Take the integer cube root of C
m, exact = gmpy2.iroot(C, 3)

if exact:
    print("Decrypted Flag:", long_to_bytes(int(m)).decode())
else:
    print("Cube root was not exact. Check your numbers.")
```

## Flag Recovery
Running the script parses the CRT and cleanly unroots the message:
`DAKSHH{n0_c0rp0_n3tw0rk_1s_s4f3_fr0m_rs4}`

## Educational Explanation
While RSA is highly secure when parameters are chosen properly, it is incredibly brittle to implementation shortcuts. A very small public exponent like `e=3` makes encryption fast, but if the exact same message is sent to at least `e` different receivers, the encryption can be algebraically broken without factoring any of the moduli! To fix this, real-world implementations must use randomized padding schemes (like RSA-OAEP), which ensures that even identical plaintexts result in completely different integers $m$ prior to exponentiation.
