# Vercel Deployment Guide (Static File Distribution)

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
