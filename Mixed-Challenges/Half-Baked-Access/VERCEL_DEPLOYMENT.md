# Vercel Deployment Guide

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
