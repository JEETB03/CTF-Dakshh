# ⏳ The 365th Day — CTF Challenge

> **Manipulate time if you dare.**

A browser-based CTF challenge where players must hack `localStorage` to fake a 365-day login streak, decode a Caesar cipher, and answer an OSINT question to capture the flag.

**Flag:** `dakshh{time_traveler}`

---

## 🛠️ How to Run

```bash
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🧩 Solve Walkthrough (Step-by-Step)

### Stage 1 — Faking the Login Streak

**Goal:** Unlock the Time Vault by reaching a 365-day login streak.

1. **Open the challenge page** at `http://localhost:3000`
2. You'll see a **Daily Login Streak** card showing `Current Streak: 1 day`
3. Clicking **"Claim Reward"** gives an error — you need 365 days
4. **Open DevTools** — press `F12` or `Cmd + Option + I` (Mac) / `Ctrl + Shift + I` (Windows)
5. **Check the Console** — notice the hint:
   ```
   Time travelers edit history. Maybe your browser remembers more than you think...
   ```
6. Go to the **Console** tab and type:
   ```js
   localStorage.setItem("login_streak", "365")
   ```
7. **Click "Claim Reward"** again (no need to refresh!)
8. ✅ **Stage 2 unlocks** — the Time Vault card appears

---

### Stage 2 — Decoding the Caesar Cipher

**Goal:** Use the OSINT clue to find the cipher shift, then decode the answer.

1. You'll see the **OSINT clue:**
   > *Dakshh is being hosted again at Heritage Institute after **9 years**.*

2. Below it, you'll see:
   ```
   Encoded Answer: crvn_cajnuna
   Hint: The organizers like classic encryption methods. The number of years might be the key...
   ```

3. **Connect the dots:**
   - "Classic encryption" → **Caesar Cipher**
   - "The number of years might be the key" → **shift = 9**

4. **Decode `crvn_cajnuna`** using Caesar Cipher with **shift = 9** (shift each letter back by 9):
   ```
   c(-9) = t        c(-9) = t
   r(-9) = i        a(-9) = r
   v(-9) = m        j(-9) = a
   n(-9) = e        n(-9) = e
   _    = _         u(-9) = l
                     n(-9) = e
                     a(-9) = r
   
   Result: time_traveler
   ```

5. **Type `time_traveler`** in the input box
6. **Click "Decrypt & Submit"**
7. 🎉 **Flag revealed:**
   ```
   Flag: dakshh{time_traveler}
   ```

---

### ❌ Wrong Answer?

If you enter the wrong answer, you'll see:

> ❌ Timeline mismatch. Try again.

---

## 🔑 Quick Solve (Speedrun)

```js
// Step 1: Open DevTools Console (F12)
// Step 2: Set the streak
localStorage.setItem("login_streak", "365")
// Step 3: Click "Claim Reward" on the page
// Step 4: Type "time_traveler" in the answer box and submit
// Flag: dakshh{time_traveler}
```

---

## 💡 Hints Given in the Challenge

| Hint | Where | Meaning |
|------|-------|---------|
| *"Time travelers don't wait a year… they rewrite history."* | Below streak card | Edit localStorage |
| Console message about browser memory | DevTools Console | Check localStorage |
| *"Classic encryption methods"* | Stage 2 hint | Caesar Cipher |
| *"The number of years might be the key"* | Stage 2 hint | Shift = 9 (from OSINT: 9 years) |
| Dakshh after **9 years** | OSINT question | Caesar shift value |

---

## 🏗️ Tech Stack

- **Next.js 16+** with TypeScript
- **TailwindCSS** + **shadcn/ui** components
- Cyberpunk / hacker-themed UI with neon effects

---

## 📁 Project Structure

```
app/
├── page.tsx                    # Main page (assembles everything)
├── layout.tsx                  # Root layout with dark theme
├── globals.css                 # Cyberpunk styling
├── components/
│   ├── streak-card.tsx         # Login streak + localStorage logic
│   └── vault-question.tsx      # Stage 2: OSINT + cipher + flag
└── utils/
    └── caesar.ts               # Caesar cipher encode/decode
```
