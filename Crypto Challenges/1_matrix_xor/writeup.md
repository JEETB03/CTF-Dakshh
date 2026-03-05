# Neo's Broken RNG - Writeup

**Difficulty:** Easy
**Flag:** `DAKSHH{n30_f0und_th3_r3d_p1ll_x0r}`

## CTFd Room Description
> "Wake up... The Matrix has you." 
> 
> We've intercepted a highly irregular transmission bleeding from a rogue Access Node near Zion. The Agents claim their proprietary encryption is mathematically flawless, but our operators think they're running a sloppy algorithm. We've managed to isolate the encrypted hex stream and the core logic of their encryption node. 
> 
> Take the red pill, dive into the code, and show them just how deep the rabbit hole really goes. Can you break the cipher and extract the hidden data?

## Initial Recon
Players are provided with `encrypt.cpp` and `output.txt`. 
Looking at the C++ code, we see the function `xor_encrypt` taking a `message` and iterating over its length, XORing every byte with a static `key`. The key is a `char` (a single 8-bit byte), which makes this a Single-Byte XOR cipher.

## Cryptographic Analysis
XOR is symmetric. If `C = P ^ K`, then `K = C ^ P`. 
We know the flag format for the DAKSHH CTF is `DAKSHH{`. We can use this known plaintext to recover the key from the ciphertext.

In `output.txt`, we see the hex string: `6e6b617962625158194e751b5975591a75595f59755d1b5e4275521a5857` (or similar).
If we take the first byte of the hex (`0x6e`, decimal 110) and XOR it with the first character of our known plaintext (`D`, decimal 68):
`110 ^ 68 = 42`. 
The key is 42 (or `*` in ASCII).

## Exploitation Steps
We can write a quick Python script to reverse the operation using our recovered key on the provided hex string.

```python
import binascii

# Extracted from output.txt
ciphertext_hex = "6e6b617962625158194e751b5975591a75595f59755d1b5e4275521a5857"
ciphertext = binascii.unhexlify(ciphertext_hex)

key = 42
plaintext = bytes([b ^ key for b in ciphertext])
print(plaintext.decode())
```

## Flag Recovery
Running the script yields:
`DAKSHH{n30_f0und_th3_r3d_p1ll_x0r}`

## Educational Explanation
A single-byte XOR cipher translates each byte to exactly one other byte, which maintains frequency distributions. Even if the key wasn't easily discoverable via Known Plaintext Attack (KPA) using the flag, it could be easily brute-forced since there are only 256 possible keys! Real-world transmission encryption should always rely on vetted protocols like AES.
