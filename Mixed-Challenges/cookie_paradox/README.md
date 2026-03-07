# Guest Cookie Paradox - CTF Writeup

Welcome to the **Guest Cookie Paradox** challenge! This guide explains how to solve it in a few simple steps.

## The Objective
The goal of this challenge is to gain unauthorized "Admin" access to the vault and retrieve the secret flags.

## Step-by-Step Solution

### 1. Explore the Site
When you first load the website, you'll see a login screen. Since we don't know the admin password, click the **"Continue as Guest"** button. This will log you in and take you to the dashboard.

### 2. Inspect the Cookie
Accessing the vault as a guest will tell you "Access Denied." Let's see how the site remembers who we are. 
1. Open your browser's **Developer Tools** (Right-click -> Inspect, or press F12).
2. Go to the **Application** tab (or **Storage** tab in Firefox).
3. Look on the left menu for **Cookies** and select the website URL.
4. You will see a cookie named `auth_token`. Its value looks like random letters and numbers, for example: `Z3Vlc3Q6MA==`.

### 3. Decode the Cookie
This random string is actually just encoded in **Base64** (a common way to encode text, often ending in `=` or `==`). 
If we decode `Z3Vlc3Q6MA==` using a tool like [CyberChef](https://gchq.github.io/CyberChef/) or a simple online Base64 decoder, it translates to:
`guest:0`

This tells us the site simply trusts the cookie to know our role! `0` probably means "not admin".

### 4. Forge an Admin Cookie
To trick the website into thinking we are the admin, we need to create our own cookie.
1. We want our role to be admin, so let's change our text to: `admin:1`
2. Now, we need to encode `admin:1` back into Base64. 
3. Encoding `admin:1` in Base64 gives us: `YWRtaW46MQ==`

### 5. Access the Vault
1. Go back to your browser's Developer Tools where you found the cookie.
2. Double-click the value of the `auth_token` cookie and replace it with our forged value: `YWRtaW46MQ==`
3. Hit Enter to save it.
4. Now, refresh the page or click **Enter Vault**.
5. **Success!** The vault will grant you access, but instead of handing over the flag immediately, it presents you with **Stage 2: OSINT Challenge**.

### 6. Solve the OSINT Challenge
The vault gives you an intercepted message: `khulwdjh_nrondwd`. It says it's a Caesar Cipher, but the shift key is missing! The hint says: *"The shift key has been hidden where the robots aren't allowed..."*
1. In web security, where bots are prevented from visiting is usually the `robots.txt` file.
2. Navigate to `http://<your-server>/robots.txt` in your browser.
3. You will see a line that says: `Disallow: /shift-key-is-3`.
4. Now we know the **Shift is 3**.
5. Go back to [CyberChef](https://gchq.github.io/CyberChef/) or a Caesar Cipher decoder, paste `khulwdjh_nrondwd`, and set the shift to 3 (or 23 if decoding backwards).
6. The decrypted message is `heritage_kolkata`. Wrap this in the standard flag format to get the final piece of the puzzle: `dakshh{heritage_kolkata}` (Submit this to the CTF platform).


