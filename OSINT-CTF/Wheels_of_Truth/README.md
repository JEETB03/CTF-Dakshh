# 🚌 Wheels of Truth — CTF Writeup

> **Category:** OSINT  
> **Flag:** `dakshh{ditobus_4646_UY89703}`

---

## 🧩 Challenge Overview

You are given an image and must use open-source intelligence (OSINT) techniques to identify a specific bus, including its company name, route number, and vehicle registration number.

---

## 🔍 Solution Walkthrough

### Step 1 — Political Poster Clue

The bottom poster in the image shows **Rasmus Hylleberg**, a political candidate for the **Roskilde constituency**.

> This narrows the location down to **Roskilde, Denmark**.

---

### Step 2 — Storefront Clue

A **7-Eleven (7/11)** store is visible in the image. Searching for **"7-Eleven Roskilde"** on [Google Maps](https://maps.google.com) reveals only a handful of locations, making it much easier to pinpoint the exact street.

---

### Step 3 — Bus Identification

Using **Google Maps Street View** near the identified 7-Eleven location in Roskilde, the buses in the area can be inspected. The leftmost bus reveals:

| Detail           | Value      |
| ---------------- | ---------- |
| **Bus Company**  | `ditobus`  |
| **Route Number** | `4646`     |

---

### Step 4 — Vehicle Registration Lookup

Searching **"ditobus 4646"** on vehicle information databases leads to records listing full details about that specific bus.

From these databases, the registration number is found:

| Detail                  | Value       |
| ----------------------- | ----------- |
| **Registration Number** | `UY89703`   |

---

## 🏁 Flag

```
dakshh{ditobus_4646_UY89703}
```

---

## 🛠️ Tools & Techniques Used

- **Google Maps / Street View** — Geo-locating the scene
- **Google Search** — Finding 7-Eleven locations in Roskilde
- **Vehicle Registration Databases** — Looking up bus details by company and route number
- **Visual Analysis** — Reading posters and storefront signs in the image

---

## 💡 Key Takeaways

1. **Political posters** can be powerful geolocation clues — they often reference specific constituencies or regions.
2. **Recognizable storefronts** (like 7-Eleven) combined with a city name drastically reduce the search area.
3. **Street View** is invaluable for confirming on-the-ground details like bus numbers and company names.
4. **Public vehicle databases** can map a company + route number to a specific registration plate.
