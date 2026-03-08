\# 🔐 Challenge Write-up: The Last Words of the Legendary Hacker 🔐



In this challenge, you’ll be tasked with bypassing a password check in the program to reveal the hidden message left by a legendary hacker. This exercise focuses on understanding binary behavior, de-obfuscation, and working with Ghidra.



\## Challenge Overview



\- \*\*Objective:\*\* Retrieve the hidden password and bypass the check to display the secret message.

\- \*\*Difficulty:\*\* Intermediate

\- \*\*Tools Required:\*\* 

&nbsp; - Ghidra (for disassembly and decompilation)

&nbsp; - Python (for scripting and de-obfuscation)



\## Step-by-Step Solution



\### Step 1: Running the Program



When you execute the program, it prompts for a password. If you enter an incorrect password, the program displays an error message and exits. This indicates that there is a specific password we need to input to unlock the secret message.



\### Step 2: Using `strings`



Running `strings` on the binary reveals nothing useful. The password is likely obfuscated and needs to be extracted by analyzing the binary code directly.



Command:



&nbsp;   strings <binary\_name>



\### Step 3: Opening the Program in Ghidra



1\. \*\*Create a New Project\*\*: Open Ghidra, create a new project, and import the binary.

2\. \*\*Analyze the Program\*\*: Run an analysis to help Ghidra identify functions and structures in the binary.

3\. \*\*Inspecting the `main` Function\*\*: In the `main` function, we observe that it calls a function named `check\_code`, which likely verifies the entered password.



\### Step 4: Analyzing the `check\_code` Function



In the `check\_code` function, we notice three key variables:

\- `local\_28` initialized to `0x6730a39060b0d14`

\- `local\_20` initialized to `0x710672011d0c7106`

\- `local\_18` initialized to `0x3f`



The code iterates over each character, verifying the user input byte by byte with an obfuscated password by XORing each byte with `0x42`. If the comparison matches the obfuscated password, the check passes; otherwise, it fails.



\### Step 5: Writing a Python Script for De-obfuscation



The variables `local\_28` and `local\_20` are 8 bytes each, while `local\_18` is 1 byte. We’ll use these to reconstruct the obfuscated password.



\#### Step 5.1: Define Base Variables



&nbsp;   local\_28 = 0x6730a39060b0d14

&nbsp;   local\_20 = 0x710672011d0c7106

&nbsp;   local\_18 = 0x3f



\#### Step 5.2: Extracting Bytes from the Variables



Define a function to extract individual bytes from `local\_28`, `local\_20`, and `local\_18`:



&nbsp;   def extract\_bytes(value, num\_bytes=8):

&nbsp;       bytes\_list = \[]

&nbsp;       for i in range(num\_bytes):

&nbsp;           byte = (value >> (i \* 8)) \& 0xFF

&nbsp;           bytes\_list.append(byte)

&nbsp;       return bytes\_list



Using this function, extract the bytes from `local\_28`, `local\_20`, and `local\_18`, then combine them to reconstruct the obfuscated password.



\#### Step 5.3: De-obfuscating the Password



The password is XORed with `0x42`, so we can reverse the obfuscation by XORing each byte with `0x42`. This reveals the actual password.



&nbsp;   def deobfuscate\_password(obfuscated\_bytes):

&nbsp;       password\_chars = \[]

&nbsp;       for byte in obfuscated\_bytes:

&nbsp;           if byte == 0x00:

&nbsp;               break

&nbsp;           password\_chars.append(chr(byte ^ 0x42))

&nbsp;       return ''.join(password\_chars)



\#### Step 5.4: Running the Script



Combine the extracted bytes and deobfuscate them:



&nbsp;   obfuscated\_password = extract\_bytes(local\_28) + extract\_bytes(local\_20) + extract\_bytes(local\_18, num\_bytes=1)

&nbsp;   password = deobfuscate\_password(obfuscated\_password)



The output reveals the password:



\*\*Password:\*\* `VOID{H1DD3N\_C0D3}`



\### Step 6: Entering the Password in the Program



Run the program again and enter the password `VOID{H1DD3N\_C0D3}` to reveal the hidden message:



&nbsp;   Access granted!

&nbsp;   Here are the final words of the legendary hacker:

&nbsp;   "Sometimes, what you seek is hidden in the shadows..."



---



\## Conclusion



This challenge demonstrates the process of analyzing a binary, extracting obfuscated data, and using scripting to reverse engineer the password. It’s a great way to practice working with XOR obfuscation and understand the flow of binary analysis in Ghidra.



\### Key Takeaways

\- Ghidra is useful for analyzing functions, understanding the structure of a program, and examining obfuscated data.

\- XOR obfuscation is common in CTF challenges, and it can be reversed if the XOR key is known.

\- Python scripting is a powerful tool to automate de-obfuscation and byte extraction.



Good luck, and remember: sometimes, the secrets are hidden in plain sight! 🔍



---



