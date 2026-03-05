import math
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad

def baby_step_giant_step(g, h, p):
    m = int(math.ceil(math.sqrt(p - 1)))
    table = {}
    e = 1
    for j in range(m):
        table[e] = j
        e = (e * g) % p
    factor = pow(g, p - 1 - m, p)
    cur = h
    for i in range(m):
        if cur in table:
            return i * m + table[cur]
        cur = (cur * factor) % p
    return None

def decrypt_flag(shared_secret, ciphertext_hex):
    try:
        key = hashlib.sha256(str(shared_secret).encode()).digest()
        iv = b'\x00' * 16
        ciphertext = bytes.fromhex(ciphertext_hex)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), 16)
        return plaintext.decode()
    except Exception as e:
        return f"Decryption failed: {e}"

def parse_output():
    vals = {}
    try:
        with open("output.txt", "r") as f:
            for line in f:
                if " = " in line:
                    key, val = line.strip().split(" = ")
                    vals[key] = val
        return vals
    except FileNotFoundError:
        return None

data = parse_output()
if data:
    target_P = int(data["P"])
    target_G = int(data["G"])
    target_A = int(data["A"])
    target_B = int(data["B"])
    target_Cipher = data["Ciphertext"]

    print(f"[*] Target P: {target_P}")
    print("[*] Attempting to crack Private Key A using BSGS...")
    a_cracked = baby_step_giant_step(target_G, target_A, target_P)

    if a_cracked:
        print(f"[+] Found Secret A: {a_cracked}")
        shared_secret = pow(target_B, a_cracked, target_P)
        print(f"[+] Calculated Shared Secret: {shared_secret}")
        print("[*] Decrypting Flag...")
        flag = decrypt_flag(shared_secret, target_Cipher)
        print(f"\nFLAG: {flag}")
    else:
        print("[-] Failed to find private key.")
