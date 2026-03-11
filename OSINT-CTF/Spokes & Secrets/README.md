# 🚲 Spokes & Secrets — OSINT CTF Writeup

## 🏷️ Challenge Overview

| Detail       | Info                          |
|--------------|-------------------------------|
| **Category** | OSINT                         |
| **Objective**| Find the contact phone number of the bike shop |

You are given an image of a street scene in **Kyoto, Japan**. Your mission is to identify the bike shop in the image and find their **contact phone number**.

---

## 🔍 Solution Walkthrough

### Step 1 — Identify the Clue in the Image

Zoom into the image carefully. On closer inspection, you can spot a **sign** on the storefront that reads:

> **"Alex Moulton"**

This is a key clue — it refers to a specific brand/type of bicycle.

---

### Step 2 — Research "Alex Moulton"

Googling **"Alex Moulton"** returns results about the **Moulton Bicycle Company**, a British manufacturer known for small-wheeled bicycles designed by Dr. Alex Moulton.

This confirms the shop is related to Moulton bicycles, but we still need to find the exact shop in **Kyoto**.

---

### Step 3 — Narrow Down the Location

Since we know the image is from Kyoto and the shop deals in Alex Moulton bicycles, searching for:

> **"Kyoto Alex Moulton"**

returns results pointing to a shop called **Moku2+4** (also written as モク2+4), a bicycle shop in Kyoto that specializes in Moulton bikes.

---

### Step 4 — Find the Contact Number

Visit the **Moku2+4** website and navigate through their pages (typically the **About** or **Contact** page). There you'll find the shop's contact phone number.

---

## 🏁 Flag

```
dakshh{075–326–3027}
```

> ⚠️ *The flag format wraps the phone number found on the shop's website.*

---

## 📝 Key Takeaways

- **Zoom in on images** — Small details like signs and text can be critical clues.
- **Cross-reference keywords** — Combining a brand name with a known location greatly narrows search results.
- **Explore official websites** — Contact information is almost always available on business websites.

---

## 🛠️ Tools Used

| Tool              | Purpose                                    |
|-------------------|--------------------------------------------|
| Image Viewer      | Zooming into the image to read the sign    |
| Google Search     | Researching "Alex Moulton" and the shop    |
| Shop Website      | Finding the contact phone number           |
