# Sherlock's Cipher Notebook - Writeup

**Difficulty:** Medium
**Flag:** `DAKSHH{3l3m3nt4ry_my_d34r_w4ts0n_0tp}`

## CTFd Room Description
> "The game is afoot, Watson!"
> 
> A courier working for Professor Moriarty was apprehended near Baker Street carrying a peculiar Java program and a ledger of encrypted broadcasts. Moriarty's underlings are boasting across London's criminal underground that they are using a mathematically "unbreakable" One-Time Pad system to coordinate a midnight heist.
> 
> However, I suspect Moriarty's lieutenants possess more arrogance than cryptographic sense. They have made a fatal, elementary error in their implementation. Study their encryption methodology, analyze the intercepted broadcasts, and unmask their hidden message before the clock strikes twelve!

## Initial Recon
Players receive `Encrypt.java` and `ciphertexts.txt`.
Looking at the Java code, we see the `key` is heavily protected by `SecureRandom`, and it correctly uses an XOR cipher. However, the crucial error is that `random.nextBytes(key)` is only called **once**, but the `key` is used in a loop to encrypt **three different messages**. This constitutes a "Many-Time Pad" vulnerability.

## Cryptographic Analysis
A One-Time Pad is only secure if the key is used exactly one time. If a key $K$ is used to encrypt two different plaintexts $P_1$ and $P_2$, resulting in $C_1$ and $C_2$:
$$C_1 = P_1 \oplus K$$
$$C_2 = P_2 \oplus K$$

If an attacker XORs the two ciphertexts together, the key mathematically cancels out:
$$C_1 \oplus C_2 = P_1 \oplus P_2$$

The attacker is now left with the XOR sum of the two plaintexts, which contains structural language patterns that can be "crib-dragged". More easily, if the attacker knows a partial plaintext for $P_3$ (the flag format `DAKSHH{`), they can combine the ciphertexts to reveal parts of the other plaintexts!

## Exploitation Steps
Using Python to exploit the Java program's output:

```python
import binascii

# Extracted directly from ciphertexts.txt
c1_hex = "..." # Paste Broadcast 1 hex here
c2_hex = "..." # Paste Broadcast 2 hex here
c3_hex = "..." # Paste Broadcast 3 hex here

c1 = binascii.unhexlify(c1_hex)
c2 = binascii.unhexlify(c2_hex)
c3 = binascii.unhexlify(c3_hex)

# Recover parts of P1 and P2 using the known flag format in P3
known_flag = b"DAKSHH{"

def str_xor(b1, b2):
    return bytes([a ^ b for a, b in zip(b1, b2)])

# c1 ^ c3 = p1 ^ p3
# Therefore: (c1 ^ c3) ^ p3_known = p1_partial
c1_c3_xor = str_xor(c1, c3)
p1_partial = str_xor(c1_c3_xor[:len(known_flag)], known_flag)
print("P1 starts with:", p1_partial.decode()) # Output: "Watson,"

c2_c3_xor = str_xor(c2, c3)
p2_partial = str_xor(c2_c3_xor[:len(known_flag)], known_flag)
print("P2 starts with:", p2_partial.decode()) # Output: "Moriart"

# Now we guess entire phrases in P1/P2 to uncover P3
guess_p1_start = b"Watson, I have found the l"
p3_partial = str_xor(str_xor(c1[:len(guess_p1_start)], c3[:len(guess_p1_start)]), guess_p1_start)
print("P3 partially uncovered:", p3_partial.decode()) 
# Output: "DAKSHH{3l3m3nt4ry_my_d34r_w"
```

The player iteratively guesses words ("diamonds", "midnight", etc.) based on standard English to completely unmask $P_3$.

## Flag Recovery
Through crib-dragging, the player pieces together the final flag:
`DAKSHH{3l3m3nt4ry_my_d34r_w4ts0n_0tp}`

## Educational Explanation
A One-Time Pad requires the key to be as long as the plaintext, purely random, kept perfectly secret, and crucially, **never reused**. The moment a pad is reused, the cipher degrades catastrophically into a simple XOR equation that leaks structural information. Real-world systems generally prefer stream ciphers (like ChaCha20) combined with unique Nonces for every single message to prevent identical key streams.
