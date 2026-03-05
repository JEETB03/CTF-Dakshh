import random
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os

# CONFIGURATION
P = 4294967291
G = 2
FLAG = b"DAKSHH{b1g_int3g3rs_n33d_b1gg3r_st3ps}"

def encrypt_flag(shared_secret):
    key = hashlib.sha256(str(shared_secret).encode()).digest()
    iv = b'\x00' * 16
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    return ciphertext.hex()

def generate():
    print(f"Generating challenge for P={P}...")
    a_secret = random.randint(2, P-2)
    b_secret = random.randint(2, P-2)
    A_public = pow(G, a_secret, P)
    B_public = pow(G, b_secret, P)
    shared_secret = pow(B_public, a_secret, P)
    encrypted_flag = encrypt_flag(shared_secret)

    with open("output.txt", "w") as f:
        f.write(f"Diffie-Hellman Key Exchange Interception\n")
        f.write(f"----------------------------------------\n")
        f.write(f"P = {P}\n")
        f.write(f"G = {G}\n")
        f.write(f"A = {A_public}\n")
        f.write(f"B = {B_public}\n")
        f.write(f"Ciphertext = {encrypted_flag}\n")

    print(f"Success! 'output.txt' created.")
    print(f"Shared Secret: {shared_secret}")

if __name__ == "__main__":
    generate()
