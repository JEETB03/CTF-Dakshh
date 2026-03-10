import os

categories = [
    'Crypto Challenges',
    'Crypto Challenges - JK',
    'Misc Challenges',
    'Mixed-Challenges',
    'OSINT-CTF',
    'Rev Engg Challenges - NB',
    'Web App - CTF - JK',
    'Web Challenges'
]

WEB_HOSTABLE_TEMPLATE = """# Vercel Deployment Guide

This challenge is a web application and can be directly hosted on Vercel.

## Deployment Steps

1. **Prerequisites**: Ensure you have a Vercel account and the Vercel CLI installed (`npm i -g vercel`), or link this repository to your Vercel dashboard.
2. **Project Setup**:
   - If this folder contains a `package.json`, `index.html`, or an `app/` directory with a web server, navigate to this directory in your terminal.
3. **Deploy via CLI**:
   - Run `vercel` in your terminal from this directory.
   - Follow the prompts to configure the project (link to existing project or create new, default settings usually apply).
4. **Environment Variables**:
   - If this challenge requires environment variables (e.g., hidden flags in backend code), add them in the Vercel Dashboard under **Settings > Environment Variables**.
5. **Production Build**:
   - Run `vercel --prod` to deploy to a production URL.
6. **Update Platform**:
   - Once successfully deployed, copy the production URL and update the CTF platform's challenge description to point players to this new URL.
"""

NON_WEB_TEMPLATE = """# Vercel Deployment Guide (Static File Distribution)

This challenge consists of downloadable files (e.g., binaries, PCAPs, logs, scripts) and does **not** have a dynamic web application to host natively.

## Deployment Strategy for File-based Challenges

To serve this challenge effectively to players via the web, you should follow this static frontend distribution method:

1. **File Hosting**:
   - Zip the required challenge files (excluding solutions or flags).
   - Upload the ZIP file to a reliable hosting service such as **Google Drive**, **Mega**, or **Pastebin** (if it's just raw text/code).
   - Generate a direct, publicly accessible sharing link.
2. **Create a Basic Frontend (Vercel)**:
   - Create a simple `index.html` file in this directory (or a new dedicated folder).
   - Copy the challenge's "Story" or "Room Description" from the `README.md` into this HTML page.
   - Add a prominent download button/link pointing to your Google Drive/Mega URL.
3. **Deploy the Static Page**:
   - Navigate to the folder containing your new `index.html`.
   - Run `vercel` via CLI and deploy it as a static project.
   - Run `vercel --prod` for the final URL.
4. **Update Platform**:
   - Provide the Vercel URL to the CTF platform so players can read the story and securely download the challenge artifacts.
"""

for category in categories:
    if os.path.isdir(category):
        for challenge in os.listdir(category):
            challenge_path = os.path.join(category, challenge)
            if os.path.isdir(challenge_path):
                # Detect if it's likely a web app (contains index.html, package.json, app folder, server.js, app.py, Dockerfile)
                files_in_chal = os.listdir(challenge_path)
                is_web = False
                web_indicators = ['package.json', 'index.html', 'app', 'server.js', 'app.py', 'Dockerfile', 'public', 'templates']
                for item in files_in_chal:
                    if item in web_indicators:
                        is_web = True
                        break
                
                # Further check if 'app' directory exists and has web indicators inside
                if 'app' in files_in_chal and os.path.isdir(os.path.join(challenge_path, 'app')):
                     is_web = True
                
                md_path = os.path.join(challenge_path, 'VERCEL_DEPLOYMENT.md')
                with open(md_path, 'w') as f:
                    if is_web:
                        f.write(WEB_HOSTABLE_TEMPLATE)
                    else:
                        f.write(NON_WEB_TEMPLATE)
                print(f"Created VERCEL_DEPLOYMENT.md for {challenge_path} (Web: {is_web})")
