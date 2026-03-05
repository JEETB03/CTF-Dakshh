# The robots run this code to secure their communications.
# You have intercepted the output of this script (output.txt).

import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

# Standard Diffie-Hellman Setup
# P is a safe 32-bit prime
P = 4294967291
G = 2

# Alice and Bob chose random secrets (we don't know these!)
# a_secret = ???
# b_secret = ???

# They calculated public keys
# A = pow(G, a_secret, P)
# B = pow(G, b_secret, P)

# They derived a shared secret
# shared_secret = pow(B, a_secret, P)

def encrypt_flag(shared_secret, flag):
    # Use SHA256 of the shared secret as the AES Key
    key = hashlib.sha256(str(shared_secret).encode()).digest()
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(flag, 16)).hex()

# The Output provided to you in output.txt is the result of this process.
